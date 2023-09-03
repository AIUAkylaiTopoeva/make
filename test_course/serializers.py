from rest_framework import serializers
from .models import Answer, Question,UserAnswer,Test
from django.contrib.auth import get_user_model

User = get_user_model()

class HiddenIsCorrectField(serializers.BooleanField):
    def to_representation(self, value):
        context = self.context
        hide_is_correct = context.get('hide_is_correct', False)
        if hide_is_correct:
            return None
        return super().to_representation(value)

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text','is_correct']
        
    is_correct = HiddenIsCorrectField()



class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True)


    class Meta:
        model = Question
        fields = ['id', 'title', 'answer_set','test']


    def create(self, validated_data):
        answers_data = validated_data.pop('answer_set')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            is_correct = answer_data.pop('is_correct', False)  # Получаем значение is_correct
            answer = Answer.objects.create(question=question, **answer_data)
            if is_correct:
                answer.is_correct = True
                answer.save()
        return question

class TestSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True, read_only=True, context={'hide_is_correct': True})

    class Meta:
        model = Test
        fields = ['id', 'title', 'question_set']

class UserAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'selected_answers', 'correct_answers']

    selected_answers = AnswerSerializer(many=True, read_only=True)
    correct_answers = AnswerSerializer(many=True, read_only=True)
    