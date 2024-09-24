from django.urls import path
from .views import PostView,CommentView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('posts/', PostView.as_view(), name='posts'),
    path('comments/<int:post_id>/',CommentView.as_view(),name='comment')
]