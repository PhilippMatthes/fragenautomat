from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, InvalidPage

from profiles.models import Profile
from profiles.forms import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    def get_context_data(self, username):
        profile = get_object_or_404(Profile, user__username=username)

        quizzes = profile.user.quiz_set.all()
        paginator = Paginator(quizzes, 4)
        page_number_tainted = self.request.GET.get('p', 1)
        try:
            page = paginator.page(page_number_tainted)
        except InvalidPage:
            # page was empty or tainted page number was not an integer
            raise Http404

        return {
            'profile': profile,
            'page': page,
        }

    def get(self, request, username):
        context = self.get_context_data(username)

        if self.request.user.username == username:
            form = ProfileForm(instance=context['profile'])
        else:
            form = None

        return TemplateResponse(request, 'profiles/profile.html', {
            'form': form, **context
        })

    def post(self, request, username):
        context = self.get_context_data(username)

        if request.user.username != username:
            raise Http404
        form = ProfileForm(request.POST, instance=context['profile'])
        if not form.is_valid():
            return HttpResponseBadRequest()
        form.save()
        return TemplateResponse(request, 'profiles/profile.html', {
            'form': form, **context
        })


class ProfileChangeView(LoginRequiredMixin, View):
    def post(self, request, username):
        if request.user.username != username:
            raise Http404
        profile = get_object_or_404(Profile, user__username=username)
        form = ProfileForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()
        form.save()
        return TemplateResponse(request, 'profiles/profile.html', {
            'profile': profile, 'page': page, 'form': form
        })



class RegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return TemplateResponse(request, 'profiles/registration/register.html', {
            'form': form,
        })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(request, 'profiles/registration/register.html', {
                'form': form,
            })
        with transaction.atomic():
            user = form.save()
            Profile.objects.create(user=user)
        login(request, user)
        return HttpResponseRedirect('/')
