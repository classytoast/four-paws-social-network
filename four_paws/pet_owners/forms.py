from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Owner


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    date_of_birth = forms.DateField(label='Дата рождения', required=False, input_formats=['%d/%m/%Y'],
                                    widget=forms.DateInput(attrs={'class': 'form-input'}))
    about_myself = forms.CharField(label='О себе', required=False,
                                   widget=forms.Textarea(attrs={'class': 'form-input'}))
    instagram = forms.CharField(label='Инстаграмм', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
    vkontakte = forms.CharField(label='Вконтакте', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
    youtube = forms.CharField(label='Youtube', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Owner
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',
                  'avatar', 'date_of_birth', 'about_myself', 'instagram', 'vkontakte', 'youtube')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))