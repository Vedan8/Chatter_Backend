from django.db import models
from django.conf import settings

class Chat(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chats'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participant_usernames = ", ".join([user.username for user in self.participants.all()])
        return f"Chat between {participant_usernames}"

    class Meta:
        unique_together = ('id',)  # Ensures each chat is unique


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        related_name='messages',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']  # Orders messages chronologically
