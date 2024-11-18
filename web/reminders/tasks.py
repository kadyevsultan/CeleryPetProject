from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Reminder
from django.utils.timezone import now

@shared_task
def send_reminder_email(reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id, is_completed=False)
        
        context = {
            'user_name': reminder.user_id.username,
            'reminder_title': reminder.title,
            'reminder_description': reminder.description,
            'reminder_date': reminder.date,
        }

        subject = f'Напоминание: {reminder.title}'
        from_email = 'noreply@example.com'
        to_email = [reminder.user_id.email]

        text_content = f"""
        Здравствуйте, {reminder.user_id.username}!

        У вас есть новое напоминание::

        Тема:{reminder.title}
        Описание:{reminder.description}
        Дата и время напоминания: {reminder.date}
        
        Пожалуйста, убедитесь, что вы выполните это напоминание вовремя.

        Спасибо за использование нашего сервиса!
        """
        
        html_content = render_to_string('emails/reminder-email.html', context)

        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()

        reminder.is_completed = True
        reminder.save()

    except Reminder.DoesNotExist:
        print('Напоминание не найдено или завершено.')
