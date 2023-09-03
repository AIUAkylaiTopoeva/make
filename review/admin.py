from django.contrib import admin

from .models import CommentAnswer, Comment

admin.site.register(Comment)
admin.site.register(CommentAnswer)
