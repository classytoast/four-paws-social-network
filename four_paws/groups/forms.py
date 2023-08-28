from django import forms

from .models import Group


class AddOrEditGroupForm(forms.ModelForm):
    name_of_group = forms.CharField(label='Название группы',
                                    widget=forms.TextInput(attrs={'class': 'form-input'}))
    about_group = forms.CharField(label='Информация о группе', required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-input'}))
    img_of_group = forms.ImageField(label='Логотип группы',
                                    widget=forms.FileInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Group
        fields = ('name_of_group', 'about_group', 'img_of_group')
