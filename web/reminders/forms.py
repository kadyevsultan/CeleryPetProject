import datetime
from django import forms
from .models import Reminder
from django.utils import timezone

class AddReminderForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    date = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'date']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].label = 'Заголовок Напоминания'
        self.fields['description'].label = 'Описание Напоминания'
        self.fields['date'].label = 'Дата для Напоминания'
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise forms.ValidationError("Заголовок Напоминания слишком длинный.")
        return title    
    
    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 500:
            raise forms.ValidationError("Описание Напоминания слишком длинное.")
        return description
        
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now():
            raise forms.ValidationError("Дата Напоминания не может быть ранее, чем сегодня.")
        return date
    
    
class UpdateReminderForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    date = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'date']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].label = 'Заголовок Напоминания'
        self.fields['description'].label = 'Описание Напоминания'
        self.fields['date'].label = 'Дата для Напоминания'
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise forms.ValidationError("Заголовок Напоминания слишком длинный.")
        return title    
    
    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 500:
            raise forms.ValidationError("Описание Напоминания слишком длинное.")
        return description
        
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now():
            raise forms.ValidationError("Дата Напоминания не может быть ранее, чем сегодня.")
        return date