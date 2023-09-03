from rest_framework import serializers
from .models import User, Student

from django.contrib.auth import get_user_model
# from .utils import send_mail_registr
from .tasks import send_mail_registr_celery 

User = get_user_model()

class RegistSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length = 8, required = True, write_only = True)

    class Meta:
        model = User
        fields = ('email', 'password' )#, 'school_number', 'school_name', 'student_class', 'location')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return email

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = True
        user.save()
        # user.create_activation_code()
        send_mail_registr_celery.delay(user.email)
        return user

class StudentRegistration(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('school_number', 'school_name', 'student_class', 'location','first_name', 'last_name')

    def create(self, validated_data):
        user = self.context['user']  # Get the user object from the context
        student = Student.objects.create(user=user, **validated_data)
        return student


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такого пользователя нет')
        return email
