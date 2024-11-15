from celery import shared_task
from django.core.mail import send_mail
from .models import Reminder
from django.utils.timezone import now

@shared_task
def send_reminder_email(reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id, is_completed=False)
        send_mail(
            subject=f'Напоминание: {reminder.title}',
            message=f'Здравствуйте, {reminder.user_id.username}!\n\nЭто ваше напоминание:\n\n{reminder.description}\n\nДата и время напоминания: {reminder.date}',
            from_email='noreply@example.com',
            recipient_list=[reminder.user_id.email],
        )
    except Reminder.DoesNotExist:
        # Напоминание не найдено или завершено
        print('Напоминание не найдено или завершено.')
    