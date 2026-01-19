import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        
        # Check if user is authenticated
        from django.contrib.auth.models import AnonymousUser
        if not self.user or isinstance(self.user, AnonymousUser):
            print("Authentication error: User not authenticated")
            await self.close()
            return
        
        try:
            # Add to group and accept connection
            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"User {self.user.username} connected to chat {self.chat_id}")
            
        except Exception as e:
            print(f"Connection error: {e}")
            await self.close()
    
    async def disconnect(self, close_code):
        from django.contrib.auth.models import AnonymousUser
        if self.user and not isinstance(self.user, AnonymousUser):
            await self.channel_layer.group_discard(
                self.chat_group_name,
                self.channel_name
            )
            print(f"User {self.user.username} disconnected from chat {self.chat_id}")
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        
        if not message:
            print("Received message without content")
            return
        
        # Save the message in the database
        await self.create_message(self.chat_id, message, self.user)
        
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
    
    @database_sync_to_async
    def create_message(self, chat_id, content, sender):
        from .models import Chat, Message
        chat = Chat.objects.get(id=chat_id)
        message = Message.objects.create(chat=chat, sender=sender, content=content)
        return message