from django import forms

from groups.models import GroupTopic
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


class SearchGroupsFilters(forms.Form):
    name_of_group = forms.CharField(label='Название группы', required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-input'}))
    topics = forms.ModelMultipleChoiceField(label='Темы',
                                            queryset=GroupTopic.objects.all(), required=False,
                                            widget=forms.CheckboxSelectMultiple)

