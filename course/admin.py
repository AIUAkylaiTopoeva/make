from django.contrib import admin
from .models import FreeCourse,PaidCourse,EnrollForm,VideoPlayer, Category, ContactForm

admin.site.register(FreeCourse)
admin.site.register(PaidCourse)
admin.site.register(EnrollForm)
admin.site.register(VideoPlayer)
admin.site.register(Category)
admin.site.register(ContactForm)