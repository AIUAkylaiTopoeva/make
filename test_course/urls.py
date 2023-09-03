from django.urls import path,include
from rest_framework.routers import DefaultRouter


from .views import TestDetailView,UserTestResultView,UserTestAnswersView,TestViewSet,QuestionViewSet

router = DefaultRouter()

router.register('all_tests', TestViewSet) # для общего всех тестов или отдельно
router.register('question', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)), 
    path('tests/<int:pk>/', TestDetailView.as_view(), name='test-detail'), # отправка ответов на вопросы
    path('user_results/', UserTestResultView.as_view(), name='user_test_results'), # ответ какой тест ты прошел
    path('tests/<int:test_id>/answers/', UserTestAnswersView.as_view(), name='user_test_answers'), #ответы на вопросы 
    
    
]

# как мы должны отправлять ответы post запрос
# {
#   "question_ids": [2,3],
#   "question_1": [5],
#   "question_3": [10,11]
  

# }
# как мы должны создавать вопросы
# {
#     "title": "java beathy",
#     "answer_set": [
#         {
#             "text": "Answer 1",
#             "is_correct": true
#         },
#         {
#             "text": "Answer 5",
#             "is_correct": false
#         },
#                 {
#             "text": "Answer 5",
#             "is_correct": true
#         },
#                 {
#             "text": "Answer 5",
#             "is_correct": false
#         }
#     ],
#     "test": 1  // Replace with the appropriate test ID