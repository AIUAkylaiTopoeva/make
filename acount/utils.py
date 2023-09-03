from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_mail_registr(email):
    message = f'Вы успешно зарегестровались на нашем сайте.'# Пройдите активацию аккаента\n Код активациии: {activation_code}'
    send_mail('Регистрация аккаунта',
               message,
               'test@gmail.com',
                [email]
                 )
# 1 версия  
# def send_mail_password(email):
#     message = f'Мы вам отправили письмо для сброса пароля.'
#     send_mail('Восстановление пароля',
#               message,
#               'test@gmail.com',
#               [email]
#               )



# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags

# def send_activation_code(email, activation_code):
#     context = {
#         'text_detail': 'Спасибо за регистрацию',
#         'email': email,
#         'domain':'http://localhost:8000',
#         'activation_code': activation_code

#     }
#     msg_html= render_to_string('index.html',context)
#     message = strip_tags(msg_html)
#     send_mail('Account activation', message,'admin@gmail.com',[email], html_message=msg_html, fail_silently=False)
