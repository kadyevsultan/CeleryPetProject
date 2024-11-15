from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index
from django_email_verification import urls as email_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reminders/', include('reminders.urls', namespace='reminders')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('email/', include(email_urls), name='email-verification'),
    path('', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
