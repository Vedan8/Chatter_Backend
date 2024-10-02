from django.urls import path
from .views import PostView,CommentView

urlpatterns = [
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<int:post_id>/', PostView.as_view(), name='posts'),
    path('comments/<int:post_id>/',CommentView.as_view(),name='comment'),
    path('posts/<int:post_id>/like/', PostView.as_view()), 
    path('posts/<int:post_id>/unlike/', PostView.as_view()),
]