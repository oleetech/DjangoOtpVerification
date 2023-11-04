# registration/urls.py

from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('otp-verification/', views.otp_verification, name='otp_verification'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/profile/', views.profile, name='custom_profile'),


]
