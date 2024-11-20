import re
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now
from datetime import timedelta
from celery import shared_task

from .models import Reminder

@shared_task
def send_reminder_email(reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id, is_completed=False)
        actual_send_time = now()
        reminder_repeat_interval = reminder.get_repeat_interval_display()
        
        context = {
            'user_name': reminder.user_id.username,
            'reminder_title': reminder.title,
            'reminder_description': reminder.description,
            'reminder_date': reminder.date,
            'reminder_repeat_interval': reminder_repeat_interval,
            'reminder_notification_time': reminder.notification_time,
            'actual_send_time': now(),
        }

        subject = f'Напоминание: {reminder.title}'
        from_email = 'noreply@example.com'
        to_email = [reminder.user_id.email]

        text_content = f"""
        Здравствуйте, {reminder.user_id.username}!

        У вас есть новое напоминание::

        Тема:{reminder.title}
        Описание:{reminder.description}
        Дата для напоминания: {reminder.date}
        Интервал напоминания: {reminder_repeat_interval}
        Время отправки напоминания: {actual_send_time.strftime('%d %B %Y г. %H:%M')}
        
        Пожалуйста, убедитесь, что вы выполните это напоминание вовремя.

        Спасибо за использование нашего сервиса!
        """
        
        html_content = render_to_string('emails/reminder-email.html', context)

        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
        if reminder.repeat_interval == 'none':
            reminder.is_completed = True
            reminder.save()
        
        if reminder.repeat_interval != 'none':
            next_date = None
            if reminder.repeat_interval == 'daily':
                next_date = reminder.date + timedelta(days=1)
            elif reminder.repeat_interval == 'weekly':
                next_date = reminder.date + timedelta(weeks=1)
            elif reminder.repeat_interval == 'monthly':
                next_date = reminder.date + timedelta(months=1)
            
            if next_date:
                reminder.date = next_date
                reminder.is_completed = False
                reminder.save()

    except Reminder.DoesNotExist:
        pass
