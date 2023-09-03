from rest_framework import serializers
from .models import UserProfile, MyCourse, MyFavorite, CompletedTest

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class MyCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCourse
        fields = '__all__'

class MyFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyFavorite
        fields = '__all__'

class CompletedTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedTest
        fields = '__all__'
