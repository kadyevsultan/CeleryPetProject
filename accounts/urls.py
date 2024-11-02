import email
from django import template
from django.shortcuts import render
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import CustomSetPasswordForm
from .views import register_user, login_user, logout_user, profile_user, delete_account_user

app_name = 'accounts'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('email-verification-sent/', lambda request: render(request, 'accounts/email/email-verification-sent.html'), name='email-verification-sent'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile_user, name='profile'),
    path('delete-account/', delete_account_user, name='delete-account-user'),
    #ResetPassword
    path('reset-password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password/password-reset.html',
        email_template_name='accounts/password/password-reset-email.html',
        success_url=reverse_lazy('accounts:password-reset-done')
    ), name='password-reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password/password-reset-done.html'
    ), name='password-reset-done'),
    path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        form_class=CustomSetPasswordForm,
        template_name='accounts/password/password-reset-confirm.html',
        success_url=reverse_lazy('accounts:password-reset-complete')
    ), name='password-reset-confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password/password-reset-complete.html'
    ), name='password-reset-complete'),
]
