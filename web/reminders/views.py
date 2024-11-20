from asyncio import log
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib import messages
from datetime import datetime
from .models import Reminder
from .forms import AddReminderForm, UpdateReminderForm
from .tasks import send_reminder_email

@login_required(login_url='accounts:login')
def reminders_home(request):
    reminders = Reminder.objects.all().filter(user_id=request.user)
    active_reminders = Reminder.objects.all().filter(user_id=request.user, is_completed=False)
    completed_reminders = Reminder.objects.all().filter(user_id=request.user, is_completed=True)    
    current_year = datetime.now().year
    context = {
        'reminders': reminders, 
        'active_reminders': active_reminders,
        'completed_reminders': completed_reminders,
        'current_year': current_year
        }
    return render(request, 'reminders/reminders-home.html', context)

@login_required(login_url='accounts:login')
def form_valid(self, form):
    messages.success(self.request, 'Напоминание успешно создано!')
    return super().form_valid(form)


class ReminderContact(LoginRequiredMixin, CreateView):
    model = Reminder
    form_class = AddReminderForm
    success_url = '/reminders/'
    template_name = 'reminders/reminders-add.html'

    def form_valid(self, form):
        reminder = form.save(commit=False)
        reminder.user_id = self.request.user
        reminder.save()
        
        if reminder.notification_time is not None: 
            notification_time = reminder.date - reminder.notification_time
            send_reminder_email.apply_async((reminder.id,), eta=notification_time)
        else:
            send_reminder_email.apply_async((reminder.id,), eta=reminder.date)
        return super().form_valid(form)

@login_required(login_url='accounts:login')
def reminders_details(request, slug):
    reminder = get_object_or_404(Reminder, slug=slug, user_id=request.user)
    reminder_repeat_interval = reminder.get_repeat_interval_display()
    
    if reminder.notification_time is not None:
        actual_send_time = reminder.date - reminder.notification_time
        context = {
            'reminder': reminder,
            'actual_send_time': actual_send_time,
            'reminder_repeat_interval': reminder_repeat_interval
        }
    else:
        context = {
            'reminder': reminder,
            'reminder_repeat_interval': reminder_repeat_interval
        }

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