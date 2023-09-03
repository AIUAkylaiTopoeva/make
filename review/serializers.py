from rest_framework import serializers
from .models import Comment, Favorite, CommentAnswer
from course.serializers import FreeCourseSerializer, PaidCourseSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    # parent_comment_id = serializers.IntegerField(write_only=True, required=False)
    # replies = serializers.SerializerMethodField()


    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comment.objects.create(author = user, **validated_data)  # create не нужно$
        return comment
    
class CommentAnswerSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = CommentAnswer
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = CommentAnswer.objects.create(author = user, **validated_data)  # create не нужно$
        return comment
    # def get_replies(self, comment):
    #     # Получаем все ответы (дочерние комментарии) для данного комментария.
    #     replies = comment.replies.all()
    #     serializer = CommentSerializer(instance=replies, many=True)
    #     return serializer.data

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     parent_comment_id = validated_data.pop('parent_comment_id', None)

    #     if parent_comment_id:
    #         parent_comment = Comment.objects.get(pk=parent_comment_id)
    #         comment = Comment.objects.create(author=user, parent_comment=parent_comment, **validated_data)
    #     else:
    #         comment = Comment.objects.create(author=user, **validated_data)

    #     return comment

class FavoriteSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    free_course = FreeCourseSerializer(read_only=True)
    paid_course = PaidCourseSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        favorite = Favorite.objects.create(author = user, **validated_data)
        return favorite