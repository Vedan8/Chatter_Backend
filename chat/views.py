from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

User = get_user_model()

class UserListView(generics.ListAPIView):
    """
    Lists all registered users except the requesting user.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


class CreateChatView(APIView):
    """
    Creates a new chat between the authenticated user and another user identified by username.
    If a chat already exists, returns the existing chat.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({'error': 'Username is required to initiate a chat.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            participant = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User with the provided username does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if participant == request.user:
            return Response({'error': 'Cannot create a chat with yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if a chat between these two users already exists
        chat = Chat.objects.filter(
            participants=request.user
        ).filter(
            participants=participant
        ).first()
        
        if chat:
            serializer = ChatSerializer(chat)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Create a new chat
        chat = Chat.objects.create()
        chat.participants.add(request.user, participant)
        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListChatsView(generics.ListAPIView):
    """
    Lists all chats the authenticated user is part of.
    """
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.chats.all()


class ChatDetailView(generics.RetrieveAPIView):
    """
    Retrieves details of a specific chat if the user is a participant.
    """
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return self.request.user.chats.all()


class ListMessagesView(generics.ListAPIView):
    """
    Retrieves messages from a specific chat.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id, participants=self.request.user)
        return chat.messages.all()

# @method_decorator(csrf_exempt, name='dispatch')
class SendMessageView(APIView):
    """
    Sends a message to a specific chat.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
        
        message = Message.objects.create(chat=chat, sender=request.user, content=content)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
