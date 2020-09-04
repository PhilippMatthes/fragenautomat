from django.contrib import admin

from profiles.models import Profile, Token


admin.site.register(Profile)
admin.site.register(Token)
