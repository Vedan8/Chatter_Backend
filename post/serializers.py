from rest_framework import serializers
from .models import Posts,Comments

class PostSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    class Meta:
        model=Posts
        fields="__all__"

class CommentSerializer(serializers.ModelSerializer):
    post=serializers.ReadOnlyField(source='post.id')
    class Meta:
        model=Comments
        fields="__all__"