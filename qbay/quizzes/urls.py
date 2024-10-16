from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add_question/', views.add_question, name='add_question'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/available/', views.available_quizzes, name='available_quizzes'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
]

