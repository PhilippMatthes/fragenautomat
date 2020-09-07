from django.views.generic import View
from django.http import Http404, HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, InvalidPage
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.crypto import get_random_string

from profiles.models import Profile, Token
from profiles.forms import ProfileForm, RegistrationForm


class ProfileView(View):
    template_name = 'profiles/profile.html'

    def has_form_access(self, username):
        is_own_profile = self.request.user.username == username
        is_superuser = self.request.user.is_superuser
        return is_own_profile or is_superuser

    def get(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)

        quizzes = profile.user.quiz_set.order_by('-created_date')
        paginator = Paginator(quizzes, 10)
        page_number_tainted = self.request.GET.get('p', 1)
        try:
            page = paginator.page(page_number_tainted)
        except InvalidPage:
            # page was empty or tainted page number was not an integer
            raise Http404

        context = {
            'profile': profile,
            'page': page,
        }

        if self.has_form_access(username):
            context['form'] = ProfileForm(instance=profile)

        return TemplateResponse(request, 'profiles/profile.html', context)

    def post(self, request, username):
        if not self.has_form_access(username):
            raise Http404

        profile = get_object_or_404(Profile, user__username=username)
        form = ProfileForm(request.POST, instance=profile)
        if not form.is_valid():
            return HttpResponseBadRequest()
        profile = form.save(commit=False)
        icon = request.FILES.get('icon')
        if icon:
            profile.icon = icon
        profile.save()
        messages.success(request, 'Your profile was updated!')
        return redirect('profiles:profile', username=username)


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return TemplateResponse(
            request, 'profiles/registration/register.html', {'form': form}
        )

    def send_activation_link(self, user):
        token = Token.objects.create(
            value=get_random_string(length=32),
            user=user
        )
        subject = 'Activate your account for fragenautom.at'
        message = render_to_string(
            'profiles/registration/activation.html',
            request=self.request,
            context={'token': token}
        )
        if settings.DEBUG:
            print(message)
        else:
            email = EmailMessage(subject, message, to=[user.email])
            email.send()

    def post(self, request):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(
                request, 'profiles/registration/register.html', {'form': form}
            )
        user = form.save(commit=False)
        user.is_active = False
        with transaction.atomic():
            user.save()
            Profile.objects.create(user=user)
        self.send_activation_link(user)
        messages.success(
            request,
            'Your profile was successfully created! ' +
            'Please check your inbox for the activation link!'
        )
        return redirect('profiles:login')


class ActivationView(View):
    def get(self, request):
        key = request.GET.get('k')
        if not key:
            raise Http404
        token = get_object_or_404(Token, value=key)
        user = token.user
        user.is_active = True
        user.save()
        messages.success(
            request,
            'Your profile was successfully activated! ' +
            'You can now login with your credentials.'
        )
        return redirect('profiles:login')
