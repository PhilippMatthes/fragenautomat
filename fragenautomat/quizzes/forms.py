from django import forms

from quizzes.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = [
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
