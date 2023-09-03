from django.apps import AppConfig



class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acount'

    # def ready(self):
    #     import acount.signals