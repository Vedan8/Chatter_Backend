from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Posts,Comments,Like
from .serializers import PostSerializer,CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class PostView(APIView):
    permission_classes = [IsAuthenticated]

    # Create a new post
    def post(self, request,post_id=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve all posts
    def get(self, request ,post_id=None):
        data = Posts.objects.all()
        serializer = PostSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update likes for a specific post (PATCH method)
    def patch(self, request,post_id ):
        try:
            post = Posts.objects.get(id=post_id)
        except Posts.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already liked the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # User has not liked the post yet, so increment likes
            post.likes += 1
            post.save()
            return Response({"message": "Post liked successfully."}, status=status.HTTP_200_OK)
        else:
            # User has already liked the post
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        try:
            post = Posts.objects.get(id=post_id)
        except Posts.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has liked the post
        try:
            like = Like.objects.get(user=request.user, post=post)
            # User has liked the post, so remove the like and decrement likes
            like.delete()
            post.likes -= 1
            post.save()
            return Response({"message": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,post_id):
        serializer=CommentSerializer(data=request.data)
        post=Posts.objects.get(id=post_id)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    
    def get(self,request,post_id):
        data=Comments.objects.filter(post=post_id)
        serializer=CommentSerializer(data=data,many=True)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


