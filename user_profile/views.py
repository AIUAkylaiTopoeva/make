# views
from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rest_framework import permissions
from .models import UserProfile, MyCourse, MyFavorite, CompletedTest
from .serializers import UserProfileSerializer, MyCourseSerializer, MyFavoriteSerializer, CompletedTestSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]  

class MyCourseViewSet(viewsets.ModelViewSet):
    queryset = MyCourse.objects.all()
    serializer_class = MyCourseSerializer
    permission_classes = [permissions.IsAuthenticated]  

class MyFavoriteViewSet(viewsets.ModelViewSet):
    queryset = MyFavorite.objects.all()
    serializer_class = MyFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]  

class CompletedTestViewSet(viewsets.ModelViewSet):
    queryset = CompletedTest.objects.all()
    serializer_class = CompletedTestSerializer
    permission_classes = [permissions.IsAuthenticated]
