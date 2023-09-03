from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, generics
from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import FreeCourse, PaidCourse, EnrollForm, VideoPlayer, Category, ContactForm
from .serializers import FreeCourseSerializer, PaidCourseSerializer,EnrollFormSerializer, VideoPlayerSerializer, CategorySerializer, ContactFormSerializer

from review.serializers import FavoriteSerializer
from review.models import Favorite

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from reportlab.pdfgen import canvas
from django.shortcuts import HttpResponse

class PermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminUser]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]
    
class PermMixin:
    def get_permissions(self):
        if self.action in ['destroy', 'retrieve', 'list']:
            permissions = [IsAdminUser]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions] 
    
class FreeCourseView(PermissionMixin,ModelViewSet):
    queryset = FreeCourse.objects.all()
    serializer_class = FreeCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['duration']
    search_fields = ['title','category__title']

    def filter_queryset(self, queryset):
        # Применение фильтров с помощью DjangoFilterBackend
        queryset = super().filter_queryset(queryset)
        return queryset

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        free_course = self.get_object()
        author = request.user
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                like = Favorite.objects.get(free_course = free_course, author=author)
                like.delete()
                message  = 'unsaved'
            except Favorite.DoesNotExist:
                Favorite.objects.create(free_course = free_course, author=author)
                message = 'saved'
            return Response(message, status=200)

class PaidCourseView(PermissionMixin,ModelViewSet):
    queryset = PaidCourse.objects.all()
    serializer_class = PaidCourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['duration', 'price']
    search_fields = ['title','category__title']

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        paid_course = self.get_object()
        author = request.user
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                like = Favorite.objects.get(paid_course = paid_course, author=author)
                like.delete()
                message  = 'unsaved'
            except Favorite.DoesNotExist:
                Favorite.objects.create(paid_course = paid_course, author=author)
                message = 'saved'
            return Response(message, status=200)


class EnrollFormViewSet(PermMixin,ModelViewSet):
    queryset = EnrollForm.objects.all()
    serializer_class = EnrollFormSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['date']

class VideoPlayerView(PermissionMixin, ModelViewSet):
    queryset = VideoPlayer.objects.all()
    serializer_class = VideoPlayerSerializer

class CategoryViewSet(PermissionMixin,ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ContactViewSet(PermMixin,ModelViewSet):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['date']


def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="enroll_forms.pdf"'

    # Создаем объект canvas для рисования в PDF
    p = canvas.Canvas(response)

    # Получаем все объекты EnrollForm из базы данных
    enroll_forms = EnrollForm.objects.all()

    # Начинаем создавать PDF-документ
    p.drawString(100, 800, "Список заполнивших форму")

    y = 750  # Начальная координата y для текста

    for form in enroll_forms:
        form_text = f"Имя: {form.first_name} {form.last_name}, Телефон: {form.phone_number}, Дата: {form.date}"
        p.drawString(100, y, form_text)
        y -= 20  # Уменьшаем координату y для следующей записи

    p.showPage()
    p.save()

    return response


def gener_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="enroll_forms.pdf"'

    # Создаем объект canvas для рисования в PDF
    p = canvas.Canvas(response)

    # Получаем все объекты EnrollForm из базы данных
    contact_forms = ContactForm.objects.all()

    # Начинаем создавать PDF-документ
    p.drawString(100, 800, "Список заполнивших форму")

    y = 750  # Начальная координата y для текста

    for form in contact_forms:
        form_text = f"Имя: {form.first_name} {form.last_name}, Телефон: {form.phone_number}, Дата: {form.date}"
        p.drawString(100, y, form_text)
        y -= 20  # Уменьшаем координату y для следующей записи

    p.showPage()
    p.save()

    return response