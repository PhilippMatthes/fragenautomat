from django.views.generic import View
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage

from huey.contrib.djhuey import db_task

from quizzes.models import Quiz


@db_task()
def increment_views(quiz):
    quiz.views += 1
    quiz.save()


class QuizView(View):
    def get(self, request, quiz_slug):
        quiz = get_object_or_404(Quiz, slug=quiz_slug)

        questions = quiz.question_set.order_by('id')
        paginator = Paginator(questions, 1)
        page_number_tainted = request.GET.get('p', 1)

        if page_number_tainted == 1:
            increment_views(quiz)

        try:
            page = paginator.page(page_number_tainted)
        except InvalidPage:
            # page was empty or tainted page number was not an integer
            raise Http404

        return TemplateResponse(request, 'quizzes/quiz.html', {
            'quiz': quiz,
            'page': page
        })
