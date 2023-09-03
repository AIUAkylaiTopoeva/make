from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле не может быть пустым')
        email = self.normalize_email(email)
        user = self.model(email= email, **extra_fields)
        user.set_password(password)
        # user.create_activation_code()
        user.save()
        return user

    def create_user(self, email, password,**extra_fields):
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fieldes):
        extra_fieldes.setdefault('is_staff', True)
        extra_fieldes.setdefault('is_active', True)
        extra_fieldes.setdefault('is_superuser', True)
        # if extra_fieldes.get('is_superuser') is not True:
        #     raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        # # Удалите поля, которые не должны быть обязательными для суперпользователя
        # for field_name in ['school_number', 'student_class', 'location', 'first_name', 'last_name']:
        #     extra_fieldes.pop(field_name, None)
        return self._create(email, password, **extra_fieldes)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20,blank=True)
    # first_name = models.CharField(max_length=30, blank=True)
    # last_name = models.CharField(max_length=30, blank=True)
    # school_number = models.IntegerField(blank=True)
    # school_name = models.CharField(max_length=100, blank=True)
    # student_class = models.CharField(max_length=50, blank=True)
    # location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []     #обязательные поля для суперпользователя

    def __str__(self) -> str:
        return f'{self.id} -> {self.email}'
    
    def has_module_perms(self, app_label):     
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    school_number = models.IntegerField(blank=False)
    school_name = models.CharField(max_length=100, blank=False)
    student_class = models.CharField(max_length=50, blank=False)
    location = models.CharField(max_length=100, blank=False)

    def __str__(self) -> str:
        return f'{self.user}'