from django.contrib.auth import get_user_model

User = get_user_model()

#Function for auth with google account
def social_create_user(backend, user=None, response=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    email = response.get('email')
    username = response.get('email').split('@')[0]  # Использовать часть email как username

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': username,
            'password': User.objects.make_random_password(),  # Генерирует случайный пароль
        }
    )

    return {
        'is_new': created,
        'user': user
    }