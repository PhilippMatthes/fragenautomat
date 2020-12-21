import pathlib

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def quiz_image_upload_path(quiz, filename):
    suffix = pathlib.Path(filename).suffix
    return f'images/{quiz.slug}/meta{suffix}'


class Quiz(models.Model):
    title = models.TextField()
    slug = models.SlugField()
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    number_of_views = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to=quiz_image_upload_path,
        null=True, blank=True
    )
    image_blurhash = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Contributor(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.user} on {self.quiz}'


def question_description_image_upload_path(question, filename):
    suffix = pathlib.Path(filename).suffix
    return f'images/{question.quiz.slug}/' + \
           f'questions/{question.id}/description{suffix}'


def question_solution_image_upload_path(question, filename):
    suffix = pathlib.Path(filename).suffix
    return f'images/{question.quiz.slug}/' + \
           f'questions/{question.id}/solution{suffix}'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    scoped_id = models.PositiveIntegerField()

    number_of_views = models.PositiveIntegerField(default=0)

    description = models.TextField(null=True, blank=True)
    description_image = models.ImageField(
        upload_to=question_description_image_upload_path,
        null=True, blank=True
    )
    description_image_blurhash = models.TextField(null=True, blank=True)

    solution = models.TextField(null=True, blank=True)
    solution_image = models.ImageField(
        upload_to=question_solution_image_upload_path,
        null=True, blank=True
    )
    solution_image_blurhash = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def page_in_quiz(self):
        # since a Django paginator starts counting with 1,
        # we need to add 1 to the 0-based scoped id
        return self.scoped_id + 1


class Contribution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']
