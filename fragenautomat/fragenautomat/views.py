from django.views.generic import View, TemplateView
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.db.models import Q, Sum

from quizzes.models import Quiz, Question
from quizzes.forms import QuizForm


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            quizzes = Quiz.objects \
                .filter(
                    Q(author=request.user) |
                    Q(is_moderated=True)
                )
        else:
            quizzes = Quiz.objects.filter(is_moderated=True)

        quizzes = quizzes.order_by('-created_date')

        query = request.GET.get('q')
        if query:
            quizzes = quizzes.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(author__username__icontains=query)
            )

        paginator = Paginator(quizzes, 9)
        page_number_tainted = request.GET.get('p', 1)
        try:
            page = paginator.page(page_number_tainted)
        except InvalidPage:
            # page was empty or tainted page number was not an integer
            raise Http404

        form = QuizForm() if request.user.is_authenticated else None

        statistics = {
            'number_of_quizzes': Quiz.objects.count(),
            'number_of_questions': Question.objects.count(),
            'number_of_views': Quiz.objects.all()\
                .aggregate(Sum('number_of_views'))['number_of_views__sum'],
        }

        return TemplateResponse(request, 'index.html', {
            'page': page,
            'form': form,
            'statistics': statistics
        })


class LegalNotesView(TemplateView):
    template_name = 'legal.html'


def not_found(request, exception=None):
    return TemplateResponse(request, 'errors/not_found.html')


def server_error(request, exception=None):
    return TemplateResponse(request, 'errors/server_error.html')
