from django import forms

from pet_owners.models import Owner, OwnerPost, Animal, PostImage


class AddOrEditPostForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', required=False,
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    text_of_post = forms.CharField(label='Текст', required=False,
                                   widget=forms.Textarea(attrs={'class': 'form-input'}))
    animals = forms.ModelMultipleChoiceField(label='укажите, про каких питомцев пост',
                                             queryset=None, widget=forms.CheckboxSelectMultiple)

    def __init__(self, user_id, *args, **kwargs):
        super(AddOrEditPostForm, self).__init__(*args, **kwargs)
        user = Owner.objects.get(pk=user_id)
        self.fields['animals'].queryset = Animal.objects.filter(pet_owner=user)

    class Meta:
        model = OwnerPost
        fields = ('title', 'text_of_post', 'animals')


class AddImageForm(forms.ModelForm):
    img = forms.ImageField(label='Добавьте фотку :)', required=False)

    class Meta:
        model = PostImage
        fields = ('img',)