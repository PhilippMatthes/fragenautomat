from django import forms

from profiles.models import Profile


class ProfileIconForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['icon', 'icon_blurhash']
        widgets = {
            'icon_blurhash': forms.HiddenInput(),
        }


class ProfileDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['real_name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'type': 'textarea'
            }),
        }
