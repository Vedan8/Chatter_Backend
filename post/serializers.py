from rest_framework import serializers
from .models import Posts, Comments, Like

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    isLiked = serializers.SerializerMethodField()  # Add isLiked field

    class Meta:
        model = Posts
        fields = "__all__"  # Includes all fields including isLiked

    def get_isLiked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False  # Default to False if user is not authenticated

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source='post.id')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comments
        fields = "__all__"
