from django.urls import path

from quizzes import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.get_quizzes, name='get_quizzes'),

    path('<slug:quiz_slug>/', views.QuizView.as_view(), name='quiz'),
]
