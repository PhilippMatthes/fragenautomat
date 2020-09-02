from django.views.generic import View, TemplateView
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.db.models import Q

from quizzes.models import Quiz


class IndexView(View):
    def get(self, request):
        quizzes = Quiz.objects.order_by('-created_date')
        query = request.GET.get('q')
        if query:
            quizzes = quizzes.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        paginator = Paginator(quizzes, 9)
        page_number_tainted = request.GET.get('p', 1)
        try:
            page = paginator.page(page_number_tainted)
        except InvalidPage:
            # page was empty or tainted page number was not an integer
            raise Http404
        return TemplateResponse(request, 'index.html', {
            'page': page,
        })


class LegalNotesView(TemplateView):
    template_name = 'legal.html'


def not_found(request, exception=None):
    return TemplateResponse(request, 'errors/not_found.html')


def server_error(request, exception=None):
    return TemplateResponse(request, 'errors/server_error.html')
