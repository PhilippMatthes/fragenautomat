from django.urls import path

from quizzes import views

app_name = 'quizzes'

urlpatterns = [
    path('<slug:quiz_slug>/', views.QuestionView.as_view(), name='question'),
]
