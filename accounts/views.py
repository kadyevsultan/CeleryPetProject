from asyncio import log
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django_email_verification import send_email, send_password, verify_email_view
from django.contrib import messages

User = get_user_model()

from .forms import RegistrationForm, LoginForm, UserUpdateForm

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')
            
            user = User.objects.create_user(
                username=user_username, 
                email=user_email, 
                password=user_password
            )   
            user.is_active = False
            
            send_email(user)
            
            return redirect('/accounts/email-verification-sent/')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/registration/register.html', {'form': form})
 

def login_user(request):
    form = LoginForm()
    
    if request.user.is_authenticated:
        return redirect('reminders:reminders-home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if request.user is not None:
            login(request, user)
            return redirect('reminders:reminders-home')
        else:
            messages.info(request, 'Неправильное имя пользователя или пароль')
            return redirect('accounts:login')
        
    context = {'form': form}
    return render(request, 'accounts/login/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('index')


@login_required(login_url='accounts:login')
def profile_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'accounts/profile/profile.html', context)

@login_required(login_url='accounts:login')
def delete_account_user(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('index')
    return render(request, 'accounts/profile/delete-account-user.html')