from rest_framework import serializers
from .models import FreeCourse, PaidCourse, EnrollForm, VideoPlayer, Category, ContactForm

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FreeCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeCourse
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comment'] = [ i.body for i in instance.comments.all()]
        # representation['com_ans'] = [ i.body for i in instance.comment.all()]
        return representation

class PaidCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaidCourse
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['saved'] = [i.paid_course for i in instance.saved.all()]
    #     return representation

class EnrollFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollForm
        fields = '__all__'

class VideoPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPlayer
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['comment'] = [ i.body for i in instance.comments.all()]
    #     return representation
    
class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'