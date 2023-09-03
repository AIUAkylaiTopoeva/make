from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import FreeCourseView,PaidCourseView,EnrollFormViewSet, CategoryViewSet, VideoPlayerView, ContactViewSet, generate_pdf, gener_pdf

router = DefaultRouter()
router.register('free_course',FreeCourseView)
router.register('paid_course',PaidCourseView)
router.register('categories',CategoryViewSet)
router.register('video', VideoPlayerView)
router.register('contact', ContactViewSet)
router.register('enroll', EnrollFormViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('generate_pdf/',generate_pdf, name='generate_pdf'),
    path('gener_pdf/',gener_pdf, name='generate_pdf'),
]