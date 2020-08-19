from django.views.generic import View
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage

from quizzes.models import Question, Quiz


class QuizView(View):
    def get(self, request, quiz_slug):
        quiz = get_object_or_404(Quiz, slug=quiz_slug)
        questions = quiz.question_set.order_by('id')
        return TemplateResponse(request, 'quizzes/quiz.html', {
            'quiz': quiz,
            'questions': questions,
        })


def get_quizzes(request):
    page_number_tainted = request.GET.get('p')
    paginator = Paginator(Quiz.objects.order_by('-created_date'), 3)
    try:
        page = paginator.page(page_number_tainted)
    except InvalidPage:
        # page was empty or tainted page number was not an integer
        raise Http404
    has_next = page.has_next()
    next_page_number = page.next_page_number() if has_next else None
    return JsonResponse({
        'pagination': {
            'has_next': has_next,
            'next': next_page_number,
        },
        'objects': serializers.serialize('json', page),
    })
