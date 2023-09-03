from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.viewsets import generics,ModelViewSet,ReadOnlyModelViewSet
from django.shortcuts import redirect, reverse
from django.http import JsonResponse

from .models import UserAnswer,Test ,Question, Answer
from .serializers import UserAnswerSerializer,TestSerializer,AnswerSerializer,QuestionSerializer
from .permissions import IsAdminOrAuthenticatedReadOnly,IsAuthenticatedAndOwner
from course.views import PermissionMixin

class TestViewSet(PermissionMixin,ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True, context={'hide_is_correct': True})
        return Response(serializer.data)

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]

    # def perform_create(self, serializer):
    #     # Проверка существующих вопросов и ответов по тексту
    #     existing_question = Question.objects.filter(title=serializer.validated_data['title']).first()
    #     if existing_question:
    #         serializer.instance = existing_question
    #     else:
    #         serializer.save()



class TestDetailView(generics.GenericAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        test = self.get_object()
        user = request.user
        question_ids = request.data.get('question_ids', [])  # Получаем список идентификаторов вопросов

        # Валидация: проверяем, что пользователь ответил на все вопросы
        if len(question_ids) != test.question_set.count():
            return Response({'error': 'You must answer all questions.'}, status=status.HTTP_400_BAD_REQUEST)

        # Создание объектов UserAnswer с выбранными ответами
        for question_id in question_ids:
            question = get_object_or_404(Question, id=question_id)
            answers_ids = request.data.get(f'question_{question_id}', [])  # Получаем список идентификаторов ответов

            if len(answers_ids) > 2:
                return Response({'error': 'You can select up to two answers for each question.'}, status=status.HTTP_400_BAD_REQUEST)

            # Получаем объекты ответов из идентификаторов
            answers = Answer.objects.filter(id__in=answers_ids)

            # Создаем объект UserAnswer для каждого вопроса с выбранными ответами
            user_answer = UserAnswer.objects.create(user=user, question=question)
            user_answer.answers.set(answers)  # Устанавливаем выбранные ответы

        # Вычисление общего результата теста
        total_questions = test.question_set.count()
        correct_answers = UserAnswer.objects.filter(user=user, question__test=test, answers__is_correct=True).count()
        score = (correct_answers / total_questions) * 100

        return Response({'message': 'Answers submitted successfully.', 'score': score}, status=status.HTTP_201_CREATED)
    

class UserTestResultView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        tests = Test.objects.all()
        user_results = []

        for test in tests:
            total_questions = test.question_set.count()
            user_answers = UserAnswer.objects.filter(user=user, question__test=test)
            correct_answers = UserAnswer.objects.filter(user=user, question__test=test, answers__is_correct=True).count()
            score = (correct_answers / total_questions) * 100

            user_results.append({
                'id': test.id,
                'title': test.title,
                'score': score,
                'total_questions': total_questions,
                'answered_questions': user_answers.count(),
            })

        return user_results


# class UserTestAnswersView(generics.ListAPIView):
#     serializer_class = UserAnswerSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         test_id = self.kwargs.get('test_id')
#         return UserAnswer.objects.filter(user=user, question__test_id=test_id)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)

#         # Get the correct answers for the test
#         test_id = self.kwargs.get('test_id')
#         test = Test.objects.get(pk=test_id)
#         questions = test.question_set.all()

#         # Create a dictionary to store correct answers for each question
#         correct_answers_dict = {}
#         for question in questions:
#             correct_answers = Answer.objects.filter(question=question, is_correct=True)
#             correct_answer_info = AnswerSerializer(correct_answers, many=True).data
#             correct_answers_dict[question.id] = correct_answer_info

#         # Update each user answer with information about correctness and correct answers for the question
#         for user_answer in serializer.data:
#             question_id = user_answer['question']['id']
#             selected_answers = user_answer.get('selected_answers', [])
#             selected_answer_ids = set(answer['id'] for answer in selected_answers)
#             correct_answer_ids = set(answer['id'] for answer in correct_answers_dict.get(question_id, []))
#             user_answer['is_correct'] = selected_answer_ids == correct_answer_ids
#             user_answer['correct_answers'] = correct_answers_dict.get(question_id, [])

#         return Response(serializer.data)

class UserTestAnswersView(generics.ListAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        test_id = self.kwargs.get('test_id')
        return UserAnswer.objects.filter(user=user, question__test_id=test_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        test_id = self.kwargs.get('test_id')
        test = Test.objects.get(pk=test_id)
        questions = test.question_set.all()

        correct_answers_dict = {}

        for question in questions:
            correct_answers = Answer.objects.filter(question=question, is_correct=True)
            correct_answer_info = AnswerSerializer(correct_answers, many=True, context={'hide_is_correct': True}).data
            correct_answers_dict[question.id] = correct_answer_info

        for user_answer in serializer.data:
            question_id = user_answer['question']['id']
            selected_answers = user_answer.get('selected_answers', [])
            selected_answer_ids = set(answer['id'] for answer in selected_answers)
            correct_answer_ids = set(answer['id'] for answer in correct_answers_dict.get(question_id, []))
            user_answer['is_correct'] = selected_answer_ids == correct_answer_ids
            user_answer['correct_answers'] = correct_answers_dict.get(question_id, [])

        return Response(serializer.data)