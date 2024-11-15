from typing import Any
from django import forms
from django.forms import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
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
        
        if len(email) > 254:
            raise forms.ValidationError("Почта слишком длинная.")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует.")
        
        return email
    
#custom form for reset password
class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают. Пожалуйста, попробуйте еще раз.",
        'password_too_similar': "Пароль не должен быть похож на личную информацию.",
        'password_too_short': "Пароль должен содержать не менее 8 символов.",
        'password_too_common': "Пароль слишком распространен, выберите другой.",
        'password_entirely_numeric': "Пароль не может состоять только из цифр.",
    }
    new_password1 = forms.CharField(
        label=("Новый пароль"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control",}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=("Подтвердите новый пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class": "form-control",}),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = '' 
        self.fields['new_password2'].help_text = ''

            
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm,self).__init__(*args, **kwargs)
        
        self.fields['email'].label = 'Ваша Электронная почта'
        self.fields['email'].required = True
        
    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ('password1','password2')
            
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        
        if len(email) > 254:
            raise forms.ValidationError("Почта слишком длинная.")
        
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует.")
        
        return email