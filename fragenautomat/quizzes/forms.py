from django import forms

from quizzes.models import Question, Quiz


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = [
            'number_of_views',
            'scoped_id',
            'quiz',
            'created_date',
            'updated_date',
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'type': 'textarea'
            }),
            'description_image_blurhash': forms.HiddenInput(),
            'solution': forms.Textarea(attrs={
                'type': 'textarea'
            }),
            'solution_image_blurhash': forms.HiddenInput(),
        }


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = [
            'number_of_views',
            'slug',
            'author',
            'updated_date',
            'created_date',
            'is_moderated',
        ]
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(attrs={
                'type': 'textarea'
            }),
            'image_blurhash': forms.HiddenInput(),
        }
