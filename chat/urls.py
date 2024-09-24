from django.urls import path
from .views import (
    UserListView,
    CreateChatView,
    ListChatsView,
    ChatDetailView,
    ListMessagesView,
    SendMessageView
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('chats/create/', CreateChatView.as_view(), name='create_chat'),
    path('chats/', ListChatsView.as_view(), name='list_chats'),
    path('chats/<int:id>/', ChatDetailView.as_view(), name='chat_detail'),
    path('chats/<int:chat_id>/messages/', ListMessagesView.as_view(), name='list_messages'),
    path('chats/<int:chat_id>/messages/send/', SendMessageView.as_view(), name='send_message'),
]
