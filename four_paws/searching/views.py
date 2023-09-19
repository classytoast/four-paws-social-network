from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from groups.models import Group
from pet_owners.models import Animal, Owner
from pet_owners.utils import DataMixin
from .forms import *


class SearchAnimalsView(LoginRequiredMixin, DataMixin, ListView):
    """Страница поиска питомцев на сайте"""
    model = Animal
    template_name = 'searching/search_animals_page.html'
    form_class = SearchAnimalsFilters
    context_object_name = 'animals'

    def get_queryset(self):
        filters = self.request.GET
        if filters.get('category_of_animal') or filters.get('sex'):
            if filters.get('category_of_animal') and filters.get('sex'):
                self.queryset = Animal.objects.filter(
                    category_of_animal=filters.get('category_of_animal'),
                    sex=filters.get('sex')
                )
            elif filters.get('category_of_animal'):
                self.queryset = Animal.objects.filter(
                    category_of_animal=filters.get('category_of_animal')
                )
            else:
                self.queryset = Animal.objects.filter(
                    sex=filters.get('sex')
                )
        else:
            self.queryset = Animal.objects.all()
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        animals = self.queryset
        context['title'] = "Поиск питомцев"
        context['form'] = self.form_class(self.request.GET)
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        context['user_animals_followed'] = self.get_animals_followers_of_owner(animals)
        return context


class SearchOwnersView(LoginRequiredMixin, DataMixin, ListView):
    """Страница поиска пользователей на сайте"""
    model = Owner
    template_name = 'searching/search_owners_page.html'
    form_class = SearchUsersFilters
    context_object_name = 'owners'

    def get_queryset(self):
        if self.request.GET:
            self.queryset = Owner.objects.filter(
                username__icontains=self.request.GET.get('username')
            )
        else:
            self.queryset = Owner.objects.all()
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Поиск пользователей"
        context['form'] = self.form_class(self.request.GET)
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


class SearchGroupsView(LoginRequiredMixin, DataMixin, ListView):
    """Страница поиска групп на сайте"""
    model = Group
    template_name = 'searching/search_groups_page.html'
    context_object_name = 'groups'

    def get_queryset(self):
        self.queryset = Group.objects.all()
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = self.queryset
        context['title'] = "Поиск групп"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        context['user_groups_followed'] = self.get_groups_followers(groups)
        return context
