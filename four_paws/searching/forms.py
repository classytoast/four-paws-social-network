from django import forms

from pet_owners.models import AnimalCategory, Animal, Owner

blank_choice = (('', '---------'),)
all_choices = blank_choice + Animal.GENDER


class SearchAnimalsFilters(forms.ModelForm):
    category_of_animal = forms.ModelChoiceField(label='Категория животного',
                                                queryset=AnimalCategory.objects.all(), required=False,
                                                widget=forms.Select(attrs={'class': 'form-input'}))
    sex = forms.ChoiceField(label='Пол', choices=all_choices, required=False,
                            widget=forms.Select(attrs={'class': 'form-input'}))

    class Meta:
        model = Animal
        fields = ('category_of_animal', 'sex')


class SearchUsersFilters(forms.Form):
    username = forms.CharField(label='По логину', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))

