import urllib

from django.views.generic import View
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseBadRequest
from django.core.paginator import InvalidPage
from django.contrib import messages
from django.urls import reverse
from django.db.models.aggregates import Max
from django.db.models.functions import Coalesce

from fragenautomat.paginators import SingleItemPaginator
from fragenautomat.sanitization import clean_markdown

from quizzes.models import Quiz, Question, Contributor, Contribution
from quizzes.forms import QuestionForm


def get_next_scoped_id(quiz):
    query = Question.objects \
        .filter(quiz=quiz) \
        .aggregate(next_scoped_id=(Coalesce(Max('scoped_id'), 0) + 1))
    return query['next_scoped_id']


class CreateQuestionView(View):
    def has_quiz_access(self, quiz):
        if not self.request.user or not self.request.user.is_authenticated:
            return False
        return quiz.contributor_set \
            .filter(user=self.request.user) \
            .exists()

    def post(self, request, quiz_slug):
        quiz = get_object_or_404(Quiz, slug=quiz_slug)
        if not self.has_quiz_access(quiz):
            raise Http404

        next_scoped_id = get_next_scoped_id(quiz)
        example_description = '`This question has just been created and was not edited yet.`'
        new_question = Question.objects.create(
            quiz=quiz,
            scoped_id=next_scoped_id,
            description=example_description
        )

        messages.success(request, 'Question created successfully.')
        url = reverse('quizzes:question', kwargs={'quiz_slug': quiz_slug})
        return redirect(f'{url}?p={new_question.page_in_quiz}')


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
    def has_quiz_access(self, quiz):
        if not self.request.user or not self.request.user.is_authenticated:
            return False
        return quiz.contributor_set \
            .filter(user=self.request.user) \
            .exists()

    def get_page(self, quiz):
        paginator = QuizPaginator(quiz)
        page_number_tainted = self.request.GET.get('p', 1)
        try:
            return paginator.page(page_number_tainted)
        except InvalidPage:
            raise Http404

    def get(self, request, quiz_slug):
        quiz = get_object_or_404(Quiz, slug=quiz_slug)
        quiz.number_of_views += 1
        quiz.save()

        page = self.get_page(quiz)
        question = page.item
        question.number_of_views += 1
        question.save()

        has_quiz_access = self.has_quiz_access(quiz)
        context = {
            'quiz': quiz,
            'page': page,
            'question': question,
            'has_quiz_access': has_quiz_access,
        }
        if has_quiz_access:
            form = QuestionForm(instance=question)
            context['form'] = form
        return TemplateResponse(request, 'quizzes/question.html', context)

    def post(self, request, quiz_slug):
        quiz = get_object_or_404(Quiz, slug=quiz_slug)
        if not self.has_quiz_access(quiz):
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

        Contribution.objects.create(
            question=question, user=self.request.user
        )

        messages.success(request, 'Question updated successfully.')
        url = reverse('quizzes:question', kwargs={'quiz_slug': quiz_slug})
        return redirect(f'{url}?{urllib.parse.urlencode(request.GET)}')
