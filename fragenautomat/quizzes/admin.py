from django.contrib import admin

from quizzes.models import Quiz, Question, Contributor, Contribution


admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Contributor)
admin.site.register(Contribution)
