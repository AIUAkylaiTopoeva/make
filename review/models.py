from django.db import models
from django.contrib.auth import get_user_model

from course.models import FreeCourse,PaidCourse

User = get_user_model()

class Favorite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved', verbose_name='Сохраненные')
    free_course = models.ForeignKey(FreeCourse, on_delete=models.CASCADE, related_name='saved', verbose_name='Сохраненные', null=True)
    paid_course = models.ForeignKey(PaidCourse, on_delete=models.CASCADE, related_name='saved', verbose_name='Сохраненные', null=True)

    def __str__(self):
        if self.free_course:
            return f"Favorite: {self.free_course.title}"
        elif self.paid_course:
            return f"Favorite: {self.paid_course.title}"
        else:
            return "Favorite"

    
class Comment(models.Model):
    course = models.ForeignKey(FreeCourse, on_delete=models.CASCADE, related_name='comments', verbose_name='Лекция')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    body = models.CharField(max_length=250)
    created_at= models.DateTimeField(auto_now_add=True)
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self) -> str:
        return f'{self.body}'

class CommentAnswer(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment', verbose_name='Лекция')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment', verbose_name='Автор')
    body = models.CharField(max_length=250)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.body}'