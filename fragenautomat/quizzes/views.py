from django.views.generic import View
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from quizzes.models import Question, Quiz


class QuizView(View):
    def get(self, request, quiz_slug):
        quiz = get_object_or_404(Quiz, slug=quiz_slug)
        requested_question_id = request.GET.get('q')
        if requested_question_id:
            question = get_object_or_404(
                Question, quiz=quiz, id=requested_question_id
            )
        else:
            question = None
        questions = quiz.question_set.order_by('id')
        return TemplateResponse(request, 'quizzes/quiz.html', {
            'quiz': quiz,
            'questions': questions,
            'question': question
        })
