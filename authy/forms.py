from django import forms
from django.contrib.auth.models import User

from .models import CustomUser


class RegisterForm(forms.Form):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female')
    ]

    LANGUAGE_CHOICES = [
        ('UA', 'Ukrainian'),
        ('ENG', 'English')
    ]

    first_name = forms.CharField(label='Name', widget=forms.TextInput(attrs={
        'type': 'text', 'class': 'form-control', 'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(label='Second Name', widget=forms.TextInput(attrs={
        'type': 'text', 'class': 'form-control', 'placeholder': 'Введите Фамилию'
    }))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'type': 'text', 'class': 'form-control', 'placeholder': 'Введите имя-пользователя'
    }))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        'type': 'text', 'class': 'form-control', 'placeholder': 'Введите почту'
    }))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={
        'type': 'radio', 'name': 'gender', 'class': 'form-check-input'
    }))
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.RadioSelect(attrs={
        'type': 'radio', 'name': 'gender', 'class': 'form-check-input'
    }))
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={
        'type': 'text', 'class': 'form-control', 'placeholder': 'Укажите ваш город'
    }))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={
        'type': 'text', 'class': 'form-control', 'placeholder': 'Введите номер телефона'
    }))
    birth_date = forms.DateField(label='Birth date', widget=forms.TextInput(attrs={
        'type': 'date', 'class': 'form-control'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'type': 'password', 'class': 'form-control', 'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput(attrs={
        'type': 'password', 'class': 'form-control', 'placeholder': 'Повторите пароль'
    }))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('Пользователь уже существует')

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError('Почта уже зарегестрирована')

    def clean_phone(self):
        cd = self.cleaned_data
        if CustomUser.objects.filter(phone_number=cd['phone']).exists():
            raise forms.ValidationError('Номер уже зарегестрирована')


class LoginAjaxForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'type': 'text', 'name': 'username', 'class': 'form-control', 'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'type': 'password', 'name': 'username', 'class': 'form-control', 'placeholder': 'Введите пароль'
    }))
