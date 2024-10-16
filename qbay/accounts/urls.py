from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    #path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
