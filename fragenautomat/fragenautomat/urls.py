from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views

from fragenautomat import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.IndexView.as_view(), name='index'),
    path("legal/", views.LegalNotesView.as_view(), name="legal"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegistrationView.as_view(), name="registration"),

    path('quizzes/', include('quizzes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
