from django.views.generic import View
from django.template.response import TemplateResponse

from quizzes.models import Quiz


class IndexView(View):
    def get(self, request):
        quizzes = Quiz.objects.all()
        return TemplateResponse(request, 'index.html', {
            'quizzes': quizzes,
        })
