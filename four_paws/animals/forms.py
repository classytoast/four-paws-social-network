from django import forms

from pet_owners.models import Animal, AnimalCategory


class AddOrEditAnimalForm(forms.ModelForm):
    name_of_animal = forms.CharField(label='Имя',
                                     widget=forms.TextInput(attrs={'class': 'form-input'}))
    animal_breed = forms.CharField(label='Порода', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-input'}))
    category_of_animal = forms.ModelChoiceField(label='Категория животного',
                                                queryset=AnimalCategory.objects.all(),
                                                widget=forms.Select(attrs={'class': 'form-input'}))
    date_of_animal_birth = forms.DateField(label='Дата рождения', required=False,
                                           input_formats=['%d.%m.%Y'],
                                           widget=forms.DateInput(attrs={'class': 'form-input'}))
    about_pet = forms.CharField(label='О питомце', required=False,
                                widget=forms.Textarea(attrs={'class': 'form-input'}))
    sex = forms.ChoiceField(label='Пол', choices=Animal.GENDER,
                            widget=forms.Select(attrs={'class': 'form-input'}))
    animal_photo = forms.ImageField(label='фото питомца',
                                    widget=forms.FileInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Animal
        fields = ('name_of_animal', 'category_of_animal', 'animal_breed',
                  'date_of_animal_birth', 'sex', 'animal_photo', 'about_pet')