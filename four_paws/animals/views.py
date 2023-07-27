from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, \
    CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from pet_owners.utils import DataMixin
from pet_owners.models import Animal


class AnimalsHome(LoginRequiredMixin, DataMixin, ListView):
    """Страница питомцев юзера"""
    model = Animal
    template_name = 'animals/animals_page.html'
    context_object_name = 'animals'

    def get_queryset(self):
        self.queryset = Animal.objects.filter(
            pet_owner__pk=self.request.user.id).annotate(
            foll_count=Count('followers')).order_by('-foll_count')
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        animals = self.queryset
        context['title'] = "Мои питомцы"
        context.update(self.get_left_menu())
        context['user_animals_followed'] = self.get_animals_followers_of_owner(animals)
        return context


class CreateAnimal(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddOrEditAnimalForm
    template_name = 'animals/add_animal_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление питомца"
        context.update(self.get_left_menu())
        return context

    def form_valid(self, form):
        form.instance.pet_owner = self.request.user
        form.save()
        return redirect('all_animals_page')


class UpdateAnimal(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = AddOrEditAnimalForm
    template_name = 'animals/edit_animal_page.html'

    def get_queryset(self):
        return Animal.objects.filter(pk=self.kwargs['pk'],
                                     pet_owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование данных питомца"
        context.update(self.get_left_menu())
        return context

    def form_valid(self, form):
        if 'update' in self.request.POST:
            form.save()
        return redirect('all_animals_page')


class DeleteAnimal(LoginRequiredMixin, DataMixin, DeleteView):
    model = Animal
    template_name = 'animals/delete_animal_page.html'
    success_url = reverse_lazy('all_animals_page')

    def get_queryset(self):
        qs = super(DeleteAnimal, self).get_queryset()
        return qs.filter(pet_owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Удаление питомца"
        context.update(self.get_left_menu())
        return context
