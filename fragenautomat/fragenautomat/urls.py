from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from fragenautomat import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.IndexView.as_view(), name='index'),
    path('legal/', views.LegalNotesView.as_view(), name='legal'),

    path('404/', views.not_found, name='not_found'),
    path('500/', views.server_error, name='server_error'),

    path('quizzes/', include('quizzes.urls')),
    path('profiles/', include('profiles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = 'fragenautomat.views.not_found'
handler500 = 'fragenautomat.views.server_error'
