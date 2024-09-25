from django.contrib import admin
from django.urls import path, include
from .views import HomeView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/', include('chat.urls')),
    path('api/', include('post.urls')),
    path('', HomeView.as_view(), name='home'),
]