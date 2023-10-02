from django import forms

from .models import PostComment


class AddOrEditCommentForm(forms.ModelForm):
    comment = forms.CharField(label='Текст комментария',
                              widget=forms.Textarea(attrs={'class': 'form-input'}))

    class Meta:
        model = PostComment
        fields = ('comment',)


class AddOrEditGroupCommentForm(forms.ModelForm):
    comment = forms.CharField(label='Текст комментария',
                              widget=forms.Textarea(attrs={'class': 'form-input'}))

    class Meta:
        model = PostComment
        fields = ('comment',)
