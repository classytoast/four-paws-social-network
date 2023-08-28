from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from pet_owners.utils import DataMixin


class GroupsHome(LoginRequiredMixin, DataMixin, ListView):
    """Страница групп юзера"""
    model = Group
    template_name = 'groups/groups_page.html'
    context_object_name = 'groups'

    def get_queryset(self):
        self.queryset = Group.objects.filter(
            members__member=self.request.user).annotate(
            mem_count=Count('members')).order_by('-mem_count')
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = self.queryset
        context['title'] = "Мои группы"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context
