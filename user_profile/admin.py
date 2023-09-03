# admin.py
from django.contrib import admin
from .models import UserProfile, MyCourse, MyFavorite, CompletedTest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'number_school')
    search_fields = ('user__username', 'email', 'town', 'class_school')

@admin.register(MyCourse)
class MyCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    search_fields = ('user__username', 'course__title')

@admin.register(MyFavorite)
class MyFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'favorites')
    search_fields = ('user__username', 'favorites__title')

@admin.register(CompletedTest)
class CompletedTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    search_fields = ('user__username', 'course__title')

