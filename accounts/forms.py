from typing import Any
from django import forms
from django.forms import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].label = 'Введите ваш email'
        self.fields['email'].required = True
        self.fields['username'].help_text = ''
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Введите пароль'
        self.fields['password1'].help_text = ''
        self.fields['password2'].label = 'Подтвердите пароль'
        self.fields['password2'].help_text = ''
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        
        if User.objects.filter(email=email).exists() and len(email) > 254:
            raise forms.ValidationError("Пользователь с такой почтой уже существует или почта слишком длинная.")
        
        return email
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))