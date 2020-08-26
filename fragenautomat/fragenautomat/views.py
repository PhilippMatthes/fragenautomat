from django.views.generic import View
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
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


class LegalNotesView(View):
    def get(self, request):
        return TemplateResponse(request, 'legal.html')


class RegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return TemplateResponse(request, 'registration/register.html', {
            'form': form,
        })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request, 'registration/register.html', {
                'form': form,
            })
        user = form.save()
        login(request, user)
        return HttpResponseRedirect('/')
