from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from quizzes.views import profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('profile/', profile_view, name='profile'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
]
