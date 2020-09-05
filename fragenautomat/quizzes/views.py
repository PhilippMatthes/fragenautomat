import urllib

from django.views.generic import View
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseBadRequest
from django.core.paginator import InvalidPage
from django.contrib import messages
from django.urls import reverse

from fragenautomat.paginators import SingleItemPaginator

from quizzes.sanitization import clean_markdown
from quizzes.models import Quiz
from quizzes.forms import QuestionForm


class QuizPaginator(SingleItemPaginator):
    def __init__(self, quiz, *args, **kwargs):
        questions = quiz.question_set.order_by('id')
        super().__init__(questions, *args, **kwargs)

    def page_or_404(self, page_number):
        try:
            return super().page(page_number)
        except InvalidPage:
            raise Http404


class QuestionView(View):
    def has_form_access(self, quiz):
        is_author = quiz.author == self.request.user
        is_superuser = self.request.user.is_superuser
        return is_author or is_superuser

    def get_page(self, quiz):
        paginator = QuizPaginator(quiz)
        page_number_tainted = self.request.GET.get('p', 1)
        try:
            return paginator.page(page_number_tainted)
        except InvalidPage:
            raise Http404

    def get(self, request, quiz_slug):
        quiz = get_object_or_404(Quiz, slug=quiz_slug)
        page = self.get_page(quiz)
        question = page.item
        context = {
            'quiz': quiz,
            'page': page,
            'question': question
        }
        if self.has_form_access(quiz):
            form = QuestionForm(instance=question)
            context['form'] = form
        return TemplateResponse(request, 'quizzes/question.html', context)

    def post(self, request, quiz_slug):
        quiz = get_object_or_404(Quiz, slug=quiz_slug)
        if not self.has_form_access(quiz):
            raise Http404

        quiz = get_object_or_404(Quiz, slug=quiz_slug)
        page = self.get_page(quiz)
        question = page.item
        form = QuestionForm(request.POST, instance=question)
        if not form.is_valid():
            return HttpResponseBadRequest()
        question = form.save(commit=False)

        question.description = clean_markdown(question.description)
        question.solution = clean_markdown(question.solution)

        description_image = request.FILES.get('description_image')
        if description_image:
            question.description_image = description_image
        solution_image = request.FILES.get('solution_image')
        if solution_image:
            question.solution_image = solution_image

        question.save()

        messages.success(request, 'Question updated successfully.')
        url = reverse('quizzes:question', kwargs={'quiz_slug': quiz_slug})
        return redirect(f'{url}?{urllib.parse.urlencode(request.GET)}')
