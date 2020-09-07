from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from profiles.models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email address',
        required=True,
        help_text='Required. We will send you a '
                  'confirmation link to that address.'
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'created_date', 'updated_date']
        widgets = {
            'description': widgets.Textarea(),
            'icon_blurhash': widgets.HiddenInput(),
        }
