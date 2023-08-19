from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

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
    avatar = forms.ImageField(label='Аватар', required=False,
                                    widget=forms.FileInput(attrs={'class': 'form-input'}))
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


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    date_of_birth = forms.DateField(label='Дата рождения', required=False, input_formats=['%d.%m.%Y'],
                                    widget=forms.DateInput(attrs={'class': 'form-input'}))
    avatar = forms.ImageField(label='Аватар', required=False,
                                    widget=forms.FileInput(attrs={'class': 'form-input'}))
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
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar',
                  'date_of_birth', 'about_myself', 'instagram', 'vkontakte', 'youtube')


class PrivacySettingsForm(forms.ModelForm):
    full_name_is_hidden = forms.BooleanField(label='Имя и фамилия', required=False,
                               widget=forms.CheckboxInput(attrs={'class': 'form-input'}))
    date_of_birth_is_hidden = forms.BooleanField(label='Дата рождения', required=False,
                             widget=forms.CheckboxInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Owner
        fields = ('full_name_is_hidden', 'date_of_birth_is_hidden')


class NewPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Cтарый пароль',
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                          "autofocus": True,
                                          'class': 'form-input'})
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'form-input'})
    )
    new_password2 = forms.CharField(
        label='Повторите новый пароль',
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'form-input'})
    )


