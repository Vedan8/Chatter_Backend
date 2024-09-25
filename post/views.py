from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Posts,Comments
from .serializers import PostSerializer,CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import cloudinary

class PostView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serilizer=PostSerializer(data=request.data)
        if serilizer.is_valid():
            serilizer.save(user=request.user)
            return Response(serilizer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serilizer.errors)
        
    def get(self,request):
        print("-----------------",cloudinary.config().cloud_name,"----------------")
        data=Posts.objects.all()
        serializer=PostSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
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


