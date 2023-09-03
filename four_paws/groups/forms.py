from django import forms

from .models import Group, GroupPost, GroupPostImage


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


class AddOrEditPostForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', required=False,
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    text_of_post = forms.CharField(label='Текст', required=False,
                                   widget=forms.Textarea(attrs={'class': 'form-input'}))

    class Meta:
        model = GroupPost
        fields = ('title', 'text_of_post')


class AddGroupImageForm(forms.ModelForm):
    img = forms.ImageField(label='Добавьте фотку :)', required=False)

    class Meta:
        model = GroupPostImage
        fields = ('img',)