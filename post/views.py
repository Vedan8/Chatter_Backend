from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Posts,Comments
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
    def patch(self, request, post_id):
        try:
            post = Posts.objects.get(id=post_id)
        except Posts.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the new likes count from the request data
        likes = request.data.get('likes', None)
        if likes is not None:
            post.likes = likes
            post.save()
            return Response({"message": "Post updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Likes field is required."}, status=status.HTTP_400_BAD_REQUEST)
        
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


