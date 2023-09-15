from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from pet_owners.models import Animal
from pet_owners.utils import DataMixin


class SearchAnimalsView(LoginRequiredMixin, DataMixin, ListView):
    """Страница поиска питомцев на сайте"""
    model = Animal
    template_name = 'searching/search_animals_page.html'
    context_object_name = 'animals'

    def get_queryset(self):
        self.queryset = Animal.objects.all()
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        animals = self.queryset
        context['title'] = "Поиск питомцев"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        context['user_animals_followed'] = self.get_animals_followers_of_owner(animals)
        return context
