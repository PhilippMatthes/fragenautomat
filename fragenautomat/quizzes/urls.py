from django.urls import path

from quizzes import views

app_name = 'quizzes'

urlpatterns = [
    path(
        '/create',
        views.CreateQuizView.as_view(),
        name='create_quiz'
    ),
    path(
        '<slug:quiz_slug>/update',
        views.UpdateQuizView.as_view(),
        name='update_quiz'
    ),
    path(
        '<slug:quiz_slug>/question/create',
        views.CreateQuestionView.as_view(),
        name='create_question'
    ),
    path(
        '<slug:quiz_slug>/question',
        views.QuestionView.as_view(),
        name='question'
    ),
]
