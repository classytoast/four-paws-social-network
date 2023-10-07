from django import forms

from .models import Group, GroupTopic
from posts.models import GroupPostImage


class AddOrEditGroupForm(forms.ModelForm):
    name_of_group = forms.CharField(label='Название группы',
                                    widget=forms.TextInput(attrs={'class': 'form-input'}))
    about_group = forms.CharField(label='Информация о группе', required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-input'}))
    img_of_group = forms.ImageField(label='Логотип группы',
                                    widget=forms.FileInput(attrs={'class': 'form-input'}))
    topics = forms.ModelMultipleChoiceField(label='Темы',
                                            queryset=GroupTopic.objects.all(), required=False,
                                            widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Group
        fields = ('name_of_group', 'about_group', 'img_of_group', 'topics')


class AddOrEditPostForm:
    pass


class AddGroupImageForm(forms.ModelForm):
    img = forms.ImageField(label='Добавьте фотку :)', required=False)

    class Meta:
        model = GroupPostImage
        fields = ('img',)
