# from allauth.socialaccount.signals import pre_social_login
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import User

# @receiver(pre_social_login)
# def populate_user_fields(sender, request, sociallogin, **kwargs):
#     user = sociallogin.user
#     if not user.email:
#         user.email = sociallogin.account.extra_data['email']
#     if not user.first_name:
#         user.first_name = sociallogin.account.extra_data['given_name']
#     if not user.last_name:
#         user.last_name = sociallogin.account.extra_data['family_name']
#     # if 'school_number' in request.data:
#     #     user.school_number = request.data['school_number']
#     # if 'school_name' in request.data:
#     #     user.school_name = request.data['school_name']
#     # if 'student_class' in request.data:
#     #     user.student_class = request.data['student_class']
#     # if 'location' in request.data:
#     #     user.location = request.data['location']

#     user.save()

# @receiver(pre_save, sender=User)
# def set_user_fields_optional(sender, instance, **kwargs):
#     if instance.is_superuser:
#         # Если пользователь является суперпользователем, делаем указанные поля необязательными
#         instance.school_number = 1
#         instance.school_name = 'None'
#         instance.student_class = 'None'
#         instance.location = 'None'
    
#     instance.save()