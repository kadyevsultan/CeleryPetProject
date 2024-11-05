from asyncio import log
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView
from datetime import datetime
from .models import Reminder
from .forms import AddReminderForm, UpdateReminderForm

@login_required(login_url='accounts:login')
def reminders_home(request):
    reminders = Reminder.objects.all().filter(user_id=request.user)
    completed_reminders = Reminder.objects.filter(user_id=request.user, is_completed=True)    
    current_year = datetime.now().year
    context = {'reminders': reminders,'completed_reminders': completed_reminders,'current_year': current_year}
    return render(request, 'reminders/reminders-home.html', context)


class ReminderContact(LoginRequiredMixin, CreateView):
    model = Reminder
    form_class = AddReminderForm
    success_url = '/reminders/'
    template_name = 'reminders/reminders-add.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

@login_required(login_url='accounts:login')
def reminders_details(request, slug):
    reminder = get_object_or_404(Reminder, slug=slug, user_id=request.user)
    context = {'reminder': reminder}
    return render(request, 'reminders/reminders-details.html', context)

@login_required(login_url='accounts:login')
def reminders_details_update(request, slug):
    model = Reminder
    form = UpdateReminderForm
    reminder = get_object_or_404(Reminder, slug=slug, user_id=request.user)
    if request.method == 'POST':
        form = UpdateReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('reminders:reminders-details', slug=slug)
    else:
        form = UpdateReminderForm(instance=reminder)
    context = {'form': form,'reminder': reminder}
    return render(request, 'reminders/reminders-details-update.html', context)

@login_required(login_url='accounts:login')
def reminders_details_delete(request, slug):
    reminder = get_object_or_404(Reminder, slug=slug, user_id=request.user)
    if request.method == 'POST':
        reminder.delete()
        return redirect('reminders:reminders-home')
    return render(request, 'reminders/reminders-confirm-delete.html', {'reminder': reminder})