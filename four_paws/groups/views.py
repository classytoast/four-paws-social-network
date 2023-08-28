from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from pet_owners.models import Owner
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
        context['user_groups_followed'] = self.get_groups_followers(groups)
        return context


class CreateGroup(LoginRequiredMixin, DataMixin, CreateView):
    """Страница создания группы"""
    form_class = AddOrEditGroupForm
    template_name = 'groups/create_group_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Создание группы"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context

    def form_valid(self, form):
        group = form.save()
        GroupMember.objects.create(
            member=self.request.user,
            group=group,
            is_owner=True,
            is_admin=True
        )
        return redirect('my_groups')


class GroupView(LoginRequiredMixin, DataMixin, ListView):
    """Страница выбранной группы"""
    model = Group
    template_name = 'groups/group_view_page.html'
    context_object_name = 'group'

    def get_queryset(self):
        self.queryset = Group.objects.get(pk=self.kwargs['id'])
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.queryset
        context['title'] = f"{group.name_of_group}"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


@login_required
def add_or_del_follower_for_group(request, group_id):
    """Добавляет или удаляет участника в группу"""
    user = Owner.objects.get(pk=request.user.id)
    group = Animal.objects.get(pk=group_id)
    try:
        GroupMember.objects.get(member=user,
                                group=group).delete()
    except GroupMember.DoesNotExist:
        GroupMember.objects.create(member=user,
                                   group=group)
    return redirect('my_groups')
