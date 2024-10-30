from django.shortcuts import render,redirect

def index(request):
    return render(request, 'index.html')

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('accounts:login')