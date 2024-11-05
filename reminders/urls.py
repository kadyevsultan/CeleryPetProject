from django.urls import path
from .views import reminders_home, ReminderContact, reminders_details, reminders_details_update, reminders_details_delete

app_name = 'reminders'

urlpatterns = [
    path('', reminders_home, name='reminders-home'),
    path('add/', ReminderContact.as_view(), name='reminders-add'),
    path('<slug:slug>/', reminders_details, name='reminders-details'),
    path('<slug:slug>/update/', reminders_details_update, name='reminders-details-update'),
    path('<slug:slug>/delete/', reminders_details_delete, name='reminders-details-delete'),
]
