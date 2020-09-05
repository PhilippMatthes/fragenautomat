from django import forms
from django.forms import widgets

from profiles.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'created_date', 'updated_date']
        widgets = {
            'description': widgets.Textarea(),
            'icon_blurhash': widgets.HiddenInput(),
        }
