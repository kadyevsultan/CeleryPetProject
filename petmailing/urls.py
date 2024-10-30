from django.contrib import admin
from django.urls import path, include
from .views import index, home
from django_email_verification import urls as email_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('home/', home, name='home'),
    path('email/', include(email_urls), name='email-verification'),
    path('', index, name='index'),
]
