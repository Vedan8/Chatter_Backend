# core/utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}. Please use this to verify your registration.'
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [email])

from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
