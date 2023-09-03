from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.authtoken.views import obtain_auth_token

from .views import PasswordResetView,PasswordResetConfirmView,UserRegistrationView #, LogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<str:uidb64>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/v1/token/', obtain_auth_token, name='api_token_auth'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
