from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, InvalidPage
from django.contrib import messages


from profiles.models import Profile
from profiles.forms import ProfileIconForm, ProfileDetailsForm


class ProfileView(TemplateView):
    template_name = 'profiles/profile.html'

    def get_context_data(self, username, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(Profile, user__username=username)

        quizzes = profile.user.quiz_set.all()
        paginator = Paginator(quizzes, 10)
        page_number_tainted = self.request.GET.get('p', 1)
        try:
            page = paginator.page(page_number_tainted)
        except InvalidPage:
            # page was empty or tainted page number was not an integer
            raise Http404

        context['profile'] = profile
        context['page'] = page

        if not self.request.user.is_authenticated:
            return context
        if not self.request.user.username == username:
            return context

        context['icon_form'] = ProfileIconForm(instance=profile)
        context['details_form'] = ProfileDetailsForm(instance=profile)
        return context


class ProfileDetailsChangeView(LoginRequiredMixin, View):
    def post(self, request, username):
        if not request.user.username == username:
            raise Http404
        profile = get_object_or_404(Profile, user__username=username)

        form = ProfileDetailsForm(request.POST, instance=profile)
        if not form.is_valid():
            return HttpResponseBadRequest()
        form.save()
        messages.success(request, 'Your profile info was updated!')
        return redirect('profiles:profile', username=username)


class ProfileIconChangeView(LoginRequiredMixin, View):
    def post(self, request, username):
        if not request.user.username == username:
            raise Http404
        profile = get_object_or_404(Profile, user__username=username)

        form = ProfileIconForm(request.POST, instance=profile)
        if not form.is_valid():
            return HttpResponseBadRequest()
        profile = form.save(commit=False)
        profile.icon = request.FILES.get('icon')
        profile.save()
        messages.success(request, 'Your profile icon was updated!')
        return redirect('profiles:profile', username=username)


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
