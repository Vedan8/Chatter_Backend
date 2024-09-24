import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import jwt
from Chatter.settings import SECRET_KEY



class ChatConsumer(AsyncWebsocketConsumer):
    from .models import Chat, Message
    from django.contrib.auth import get_user_model
    User = get_user_model()
    async def connect(self):
        self.user = None
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Parse query parameters
        query_params = parse_qs(self.scope['query_string'].decode('utf-8'))
        token = query_params.get('token')

        if not token:
            print("Authentication error: Token not provided")
            await self.close()
            return

        token = token[0]

        try:
            # Decode the token using the secret key from environment variables
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            self.user = await self.get_user(payload['user_id'])  # Use the user_id from the token
            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"User {self.user.username} connected to chat {self.chat_id}")
        except jwt.ExpiredSignatureError:
            print("Authentication error: Token has expired")
            await self.close()
        except jwt.InvalidTokenError:
            print("Authentication error: Invalid token")
            await self.close()
        except User.DoesNotExist:
            print("Authentication error: User does not exist")
            await self.close()
        except Exception as e:
            print(f"Authentication error: {e}")
            await self.close()

    async def disconnect(self, close_code):
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
        chat = Chat.objects.get(id=chat_id)
        message = Message.objects.create(chat=chat, sender=sender, content=content)
        return message

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)
