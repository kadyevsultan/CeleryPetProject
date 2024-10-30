from django.shortcuts import render
from django.urls import path
from .views import register_user, login_user, logout_user

app_name = 'accounts'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('email-verification-sent/', lambda request: render(request, 'accounts/email/email-verification-sent.html'), name='email-verification-sent'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
