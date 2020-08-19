from django.contrib import admin

from quizzes.models import Quiz, Question


admin.site.register(Question)
admin.site.register(Quiz)
