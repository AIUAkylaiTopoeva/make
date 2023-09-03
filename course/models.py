from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=120,unique=True,verbose_name='Название категории')

    def __str__(self):
        return self.title
        
class FreeCourse(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    erray = models.CharField(max_length=400, blank=True)
    duration = models.CharField(max_length=100)
    num_lectures = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    # favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

class PaidCourse(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    num_lectures = models.IntegerField()
    start_date = models.DateField()
    price = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    # favorite = models.BooleanField(default=False)

    def str(self):
        return f'{self.title}'

    
class EnrollForm(models.Model):
    course = models.ForeignKey(PaidCourse, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} - {self.phone_number} - {self.date}'


class VideoPlayer(models.Model):
    course = models.ForeignKey(FreeCourse ,on_delete=models.CASCADE, related_name='video_pl')
    title = models.CharField(max_length=100)
    # description = models.TextField()
    video = models.URLField()
    lecture = models.CharField()

    def __str__(self) -> str:
        return f'{self.title}'

class ContactForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name} - {self.phone_number}'
