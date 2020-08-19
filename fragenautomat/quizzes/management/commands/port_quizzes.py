"""Caution: This code is really dirty and only for migration from the old fragenautom.at"""

import json
import pathlib

import blurhash

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.management.base import BaseCommand

from quizzes.models import Quiz, Question


class Command(BaseCommand):
    """
    Port quizzes from the old fragenautomat. Yikes, dirty code.

    Takes the following files in the data/ subdir:
    - db.backup.json (complete database dump)
    - images/ (all uploaded media images)
    """

    def handle(self, *args, **options):

        base_dir = 'fragenautomat/quizzes/management/commands/data'
        with open(f'{base_dir}/db.backup.json', 'rb') as f:
            json_data = json.loads(f.read())

        author = User.objects.first()
        if not author:
            print('Please create a user first!')
            return

        for line in json_data:
            if line['model'] == 'quizzes.quiz':
                pk = line['pk']
                if Quiz.objects.filter(pk=pk).exists():
                    continue
                entry = line['fields']
                title = entry['title']
                description = entry['description']
                created_by = entry['created_by']
                created_at = entry['created_at']
                updated_at = entry['updated_at']
                image_filename = entry.get('image')
                if image_filename:
                    with open(f'{base_dir}/{image_filename}', 'rb') as f:
                        image = SimpleUploadedFile(image_filename, f.read())
                    with open(f'{base_dir}/{image_filename}', 'rb') as f:
                        image_hash = blurhash.encode(f, x_components=4, y_components=3)
                else:
                    image = None
                    image_hash = None
                q, c = Quiz.objects.get_or_create(
                    pk=pk,
                    title=title,
                    slug=slugify(title),
                    description=description,
                    author=author,
                    image=image,
                    image_blurhash=image_hash,
                    created_date=created_at,
                    updated_date=updated_at
                )

                print(f'{q} created: {c}, updated: {not c}')

        for line in json_data:
            if line['model'] == 'questions.textualquestion':
                pk = line['pk']
                entry = None
                if Question.objects.filter(pk=pk).exists():
                    continue
                for l in json_data:
                    if l['pk'] == pk and l['model'] == 'questions.question':
                        entry = {**l['fields'], **line['fields']}
                        break
                if entry.get('description_image'):
                    with open(f'{base_dir}/{entry["description_image"]}', 'rb') as f:
                        description_image_hash = blurhash.encode(f, x_components=4, y_components=3)
                    with open(f'{base_dir}/{entry["description_image"]}', 'rb') as f:
                        description_image = SimpleUploadedFile(
                            name=entry['description_image'],
                            content=f.read()
                        )
                else:
                    description_image_hash = None
                    description_image = None
                if entry.get('solution_image'):
                    with open(f'{base_dir}/{entry["solution_image"]}', 'rb') as f:
                        solution_image_hash = blurhash.encode(f, x_components=4, y_components=3)
                    with open(f'{base_dir}/{entry["solution_image"]}', 'rb') as f:
                        solution_image = SimpleUploadedFile(
                            name=entry['solution_image'],
                            content=f.read()
                        )
                else:
                    solution_image_hash = None
                    solution_image = None
                created_at = entry.get('created_at')
                updated_at = entry.get('updated_at')
                quiz = entry.get('quiz')
                description = entry.get('description')
                solution = entry.get('solution')
                q, c = Question.objects.get_or_create(
                    pk=pk,
                    quiz_id=quiz,
                    description=description,
                    description_image=description_image,
                    description_image_blurhash=description_image_hash,
                    solution=solution,
                    solution_image=solution_image,
                    solution_image_blurhash=solution_image_hash,
                    created_date=created_at,
                    updated_date=updated_at
                )

                print(f'{q} created: {c}, updated: {not c}')
