from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegistSerializer, StudentRegistration
from rest_framework.response import Response
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import IsActivePermission
from django.shortcuts import redirect
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework.views import APIView
# from social_django.views import AuthView, AuthCallbackView, complete

# class RegisterView(APIView):
#     @swagger_auto_schema(request_body=RegistSerializer())
#     def post(self, request):
#         data = request.data
#         serializer = RegistSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response('Successfully registered', 201)

# def registration_view(request):
#     if request.method == 'POST':
#         serializer = RegistSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response('Successfully registered', status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return render(request, 'acount/registr.html')

class UserRegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistSerializer())
    # @swagger_auto_schema(request_body=StudentRegistration())
    def post(self, request, format=None):
        user_serializer = RegistSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()  # Create the user
            student_serializer = StudentRegistration(data=request.data, context={'user': user})
            if student_serializer.is_valid():
                student_serializer.save()  # Create the student profile
                return Response({'message': 'User and student profile created successfully'}, status=status.HTTP_201_CREATED)
            else:
                user.delete()  # Delete the user if the student profile creation fails
                return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GoogleAuthView(AuthView):
#     backend = 'social_core.backends.google.GoogleOAuth2'


# class GoogleAuthCallbackView(AuthCallbackView):
#     def get(self, request, *args, **kwargs):
#         # Проверяем, был ли успешный запрос аутентификации через Google
#         if 'code' in request.GET:
#             return complete(request, 'google-oauth2')
#         else:
#             return redirect('login')  # Перенаправляем на страницу входа, если нет кода

        
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

User = get_user_model()



from .serializers import PasswordResetSerializer

class PasswordResetView(APIView):
    @swagger_auto_schema(request_body=PasswordResetSerializer())
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)

        # Кодируем идентификатор пользователя в формате base64
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Формирование ссылки на сброс пароля
        reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid})
        reset_url = request.build_absolute_uri(reset_url)

        # Создание HTML-шаблона письма
        email_subject = 'Сброс пароля'
        email_body = f'Для сброса пароля, перейдите по ссылке: {reset_url}'

        # Отправка письма с ссылкой на сброс пароля
        send_mail(
            email_subject,
            email_body,
            'noreply@example.com',
            [email],
            fail_silently=False,
        )

        return Response({'message': 'На вашу почту отправлено письмо со ссылкой на сброс пароля.'}, status=status.HTTP_200_OK)

        
    
class PasswordResetConfirmView(APIView):
    def get(self, request, uidb64):
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = get_object_or_404(User, pk=uid)

        context = {
            'uidb64': uidb64,
        }
        return render(request, 'index.html', context)
    
    @swagger_auto_schema(request_body=PasswordResetSerializer())
    def post(self, request, uidb64):
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = get_object_or_404(User, pk=uid)

        # Обработка запроса на сброс пароля
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({'message': 'Новый пароль и подтверждение пароля не совпадают.'}, status=status.HTTP_400_BAD_REQUEST)
        

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Пароль успешно сброшен.'}, status=status.HTTP_200_OK)

# class LogoutView(APIView):
#     permission_classes = [IsActivePermission]
#     def post(self,request):
#         user = request.user
#         Token.objects.filter(user=user).delete()
#         return Response('You logout from your account')


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class YourAuthTokenView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        token, created = Token.objects.get_or_create(user=user)  
        return Response({'token': token.key})
        
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise AuthenticationFailed('No authentication credentials provided')

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})     

@api_view(['POST'])
def your_auth_token_view(request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)  # Аналогично здесь
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
