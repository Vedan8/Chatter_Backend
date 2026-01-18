# core/views.py
from urllib import response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import (
    UserSerializer,
    LoginSerializer,
    OtpSerializer,
    UsernameUpdateSerializer,
    ProfileImageUpdateSerializer
)
from .utils import send_otp_email
import random
from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
import logging
import requests
# from google.oauth2 import id_token
# from google.auth.transport import requests

# Initialize logger
logger = logging.getLogger(__name__)

otp_dict = {}

def set_jwt_cookies(response, user):
    refresh = RefreshToken.for_user(user)

    response.set_cookie(
        key='access_token',
        value=str(refresh.access_token),
        httponly=True,
        secure=True,   # True in production
        samesite='None',
        path='/',
    )

    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=True,
        samesite='None',
        path='/',
    )

    return response

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = str(random.randint(100000, 999999))  # Generate random OTP
            otp_dict[request.data['email']] = otp  # Store OTP temporarily
            print(otp)
            print(otp_dict[request.data['email']])
            # Send the OTP email
            send_otp_email(request.data['email'], otp)

            return Response({'message': 'User created, OTP sent!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOtpView(APIView):
    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            user = User.objects.filter(email=email).first()
            if otp_dict.get(email) == otp:
                try:
                    refresh = RefreshToken.for_user(user)
                    user = User.objects.get(email=email)
                    user.is_active = True  # Activate the user
                    user.save()
                    del otp_dict[email]  # Remove OTP after verification
                    response = Response({
                        'access': str(refresh.access_token),
                        'message':"Otp Verified"
                        }, status=status.HTTP_200_OK)
                    response.set_cookie(
                        key='refresh_token',
                        value=str(refresh),
                        httponly=True,
                        secure=False,  # Set to True in production with HTTPS
                        samesite='Lax',  # Adjust as needed
                        max_age=86400,  # 1 day in seconds
                    )
                    return response
                except User.DoesNotExist:
                    return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Invalid OTP!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                response = Response({'username': user.username})
                return set_jwt_cookies(response, user)

            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from cookies
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token is None:
                logger.warning("Logout attempt without refresh token.")
                return Response(
                    {'error': 'Refresh token not provided.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Initialize RefreshToken object
            refresh = RefreshToken(refresh_token)
            
            # Extract user_id from the token's payload
            user_id = refresh['user_id']
            
            # Retrieve the user associated with the user_id
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                logger.error(f"User with ID {user_id} does not exist.")
                return Response(
                    {'error': 'User does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Blacklist the refresh token
            refresh.blacklist()
            
            # Clear the refresh token cookie
            response = Response({
                'message': 'Successfully logged out.',
                'user': {
                    'email': user.email,
                    'username': user.username
                }
            }, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('refresh_token')
            logger.info(f"User {user.email} logged out successfully.")
            return response

        except TokenError as e:
            logger.error(f"TokenError during logout: {str(e)}")
            return Response(
                {'error': 'Invalid or expired refresh token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception("Unexpected error during logout.")
            return Response(
                {'error': f'An error occurred during logout: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UsernameUpdateSerializer(data=request.data)
        if serializer.is_valid():
            if not serializer.validated_data['username']:
                return Response({
                    "error":"Username Required"
                })
            user = request.user
            user.username = serializer.validated_data['username']
            user.save()
            return Response({'message': 'Username updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateProfileImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfileImageUpdateSerializer(data=request.data)
        if serializer.is_valid():
            if not serializer.validated_data['profileImage']:
                return Response({
                    "error":"Image Required"
                })
            user = request.user
            user.profileImage = serializer.validated_data['profileImage']
            user.save()
            return Response({'message': 'ProfileImage updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(APIView):
    def post(self, request):
        # Get the refresh token from cookies
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({'error': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token
            return Response({'access': str(new_access)}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(APIView):
    def post(self, request):
        access_token = request.data.get('token')

        if not access_token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 🔐 Verify access token using Google UserInfo API
        google_response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        if google_response.status_code != 200:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = google_response.json()
        email=user_info.get('email')
        username=user_info.get('name')
        profileImageUrl=user_info.get('picture')
        profileImage=user_info.get('picture')
        serializer = UserSerializer(data={
            'email': email,
            'username': username,
            'profileImageUrl': profileImageUrl,
            'profileImage':profileImage,
            'password': 'default_password'
        })
        if not User.objects.filter(email=email).exists():
            if serializer.is_valid():
                serializer.save()
        user=User.objects.filter(email=email).first()
        user.is_active = True
        user.save()
        response = Response({'username': user.username})
        return set_jwt_cookies(response, user)

        