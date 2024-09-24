# core/urls.py

from django.urls import path
from .views import (
    RegisterView,
    VerifyOtpView,
    LoginView,
    LogoutView,
    UpdateUsernameView,
    TokenRefreshView,
    UpdateProfileImageView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-username/', UpdateUsernameView.as_view(), name='update-username'),
    path('update-profileImage/', UpdateProfileImageView.as_view(), name='update-profileImage'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
