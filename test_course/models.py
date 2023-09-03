from django.db import models
from django.contrib.auth import get_user_model

from course.models import  FreeCourse#VideoPlayer

User = get_user_model()

class Test(models.Model):
    free_course = models.ForeignKey(FreeCourse, null=True, blank=True, on_delete=models.CASCADE)
    # paid_course = models.ForeignKey(PaidCourse, null=True, blank=True, on_delete=models.CASCADE)
    # video = models.ForeignKey(VideoPlayer,null=True, blank=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # is_multiple_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
    def clone(self):
        # Создаем клон объекта Answer без сохранения
        return Answer(id=self.id, text=self.text, question=self.question)


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer)
    # answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    # selected_answers = models.ManyToManyField(Answer)
    # is_correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.question.title} {self.answers}'