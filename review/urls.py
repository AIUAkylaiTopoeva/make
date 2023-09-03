from django.urls import path, include
from .views import CommentViewSet, CommentAnswerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('comments', CommentViewSet)
router.register('com_ans', CommentAnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
