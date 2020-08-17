from django.urls import path

from quizzes import views

urlpatterns = [
    path('<slug:quiz_slug>/', views.QuizView.as_view(), name='quiz'),
]
