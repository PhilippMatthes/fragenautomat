from django.contrib import admin
from django.urls import path, include

from fragenautomat import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.IndexView.as_view(), name='index'),

    path('quizzes/', include('quizzes.urls')),
]
