# urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, MyCourseViewSet, MyFavoriteViewSet, CompletedTestViewSet

router = DefaultRouter()
router.register('userprofiles', UserProfileViewSet)
router.register('mycourses', MyCourseViewSet)
router.register('myfavorites', MyFavoriteViewSet)
router.register('completedtests', CompletedTestViewSet)

urlpatterns = [
     path('', include(router.urls))
]
