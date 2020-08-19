from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from fragenautomat import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.IndexView.as_view(), name='index'),

    path('quizzes/', include('quizzes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
