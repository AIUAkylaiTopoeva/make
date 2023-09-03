from django.contrib import admin

from django.contrib import admin
from .models import Question, Answer,UserAnswer,Test

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    
admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer)