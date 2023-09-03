# models
from django.db import models

from django.db import models
from acount.models import User
from course.models import FreeCourse  # Favorite
from review.models import Favorite
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, default='')
    last_name = models.CharField(max_length=250, default='')
    town = models.CharField(max_length=250)
    class_school = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    number_school = models.CharField(max_length=250)
    address_school = models.CharField(max_length=250)
    number_telephone = models.CharField(max_length=250)
    image = models.ImageField(
        upload_to='user_profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MyCourse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        FreeCourse, related_name='mycourses', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.course}"


class MyFavorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ForeignKey(
        Favorite, related_name='myfavorites', on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.user} - {self.favorites}"


class CompletedTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        FreeCourse, related_name='completed_tests', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.course}"
