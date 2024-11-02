from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

@login_required(login_url='accounts:login')
def home(request):
    current_year = datetime.now().year
    context = {'current_year': current_year}
    return render(request, 'home.html', context)
