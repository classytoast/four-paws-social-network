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
        self.queryset = Group.objects.get(pk=self.kwargs['group_id'])
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.queryset
        context['title'] = f"{group.name_of_group}"
        posts = GroupPost.objects.filter(group=group)
        auth_user = Owner.objects.get(pk=self.request.user.id)
        context['data_for_post'] = self.get_data_for_post(posts, auth_user)
        context['name_page_for_likes'] = 'group_view'
        context.update(self.get_left_menu())
        context.update(self.get_right_menu(auth_user))
        context['user_groups_followed'] = self.get_groups_followers([group])
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


class CreateGroupPostView(LoginRequiredMixin, DataMixin, CreateView):
    """Страница создания поста в группу"""
    form_class = AddOrEditPostForm
    template_name = 'groups/add_group_post_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление поста в группу"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context

    def form_valid(self, form):
        form.instance.group = self.kwargs['group_id']
        post = form.save()
        if 'add_photos' in self.request.POST:
            return redirect('add_images_to_group_post',
                            group_id=self.kwargs['group_id'],
                            post_id=post.pk)
        elif 'to_publish' in self.request.POST:
            return redirect('show_group', group_id=self.kwargs['group_id'])


class AddGroupImgsView(LoginRequiredMixin, DataMixin, CreateView):
    """Страница добавления изображений к посту"""
    form_class = AddGroupImageForm
    template_name = 'groups/add_group_images.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление изображений"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        post = GroupPost.objects.get(pk=self.kwargs['post_id'])
        context['added_images'] = post.images.all()
        return context

    def form_valid(self, form):
        if form.instance.img:
            post = GroupPost.objects.get(pk=self.kwargs['post_id'])
            if post.autor == self.request.user:
                form.instance.owner = self.request.user
                form.instance.post = post
                form.save()
        if 'add_more_photos' in self.request.POST:
            return redirect('add_images_to_group_post', post_id=post.pk)
        elif 'to_publish' in self.request.POST:
            return redirect('show_group', group_id=self.kwargs['group_id'])