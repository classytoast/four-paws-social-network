from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from pet_owners.models import Owner
from posts.models import GroupPost
from posts.utils import PostDataMixin
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


class GroupView(LoginRequiredMixin, DataMixin, PostDataMixin, ListView):
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
        all_posts = GroupPost.objects.filter(group=group)
        context['members'] = Owner.objects.filter(group_subscriptions__group=group)[:9]
        context['all_posts'] = all_posts
        context['topics'] = group.topics.all()
        context['user_groups_followed'] = self.get_groups_followers([group])
        context['data_for_post'] = self.get_data_for_posts(all_posts, type_of_posts='group-post')
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


@login_required
def add_or_del_follower_for_group(request, group_id):
    """Добавляет или удаляет участника в группу"""
    user = request.user
    group = Group.objects.get(pk=group_id)
    try:
        GroupMember.objects.get(member=user,
                                group=group).delete()
    except GroupMember.DoesNotExist:
        GroupMember.objects.create(member=user,
                                   group=group)
    return redirect('my_groups')


class UpdateGroupPostView(LoginRequiredMixin, DataMixin, UpdateView):
    """Страница редактирования поста в группе"""
    form_class = AddOrEditPostForm
    template_name = 'posts/edit_post_page.html'

    def get_queryset(self):
        return GroupPost.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование поста в группе"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context

    def form_valid(self, form):
        if 'cancel' in self.request.POST:
            return redirect('show_group', group_id=self.kwargs['group_id'])
        post = form.save()
        if 'update_without_photos' in self.request.POST:
            return redirect('show_group', group_id=self.kwargs['group_id'])
        elif 'update_with_photos' in self.request.POST:
            return redirect('add_images_to_group_post',
                            group_id=self.kwargs['group_id'],
                            post_id=post.pk)


class DeleteGroupPost(LoginRequiredMixin, DataMixin, DeleteView):
    """Страница удаления поста в группе"""
    model = GroupPost
    template_name = 'posts/delete_post_page.html'

    def get_success_url(self):
        return reverse_lazy('show_group', kwargs={'group_id': self.kwargs['group_id']})

    def get_queryset(self):
        qs = super(DeleteGroupPost, self).get_queryset()
        if GroupMember.objects.get(member=self.request.user, group=self.kwargs['group_id']).is_admin:
            return qs
        else:
            return None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Удаление поста в группе"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


class GroupMembersView(DataMixin, ListView):
    """Страница участников в выбранной группе"""
    model = Group
    template_name = 'groups/group_followers_page.html'
    context_object_name = 'group'

    def get_queryset(self):
        self.queryset = Group.objects.get(pk=self.kwargs['group_id'])
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.queryset
        context['members'] = Owner.objects.filter(group_subscriptions__group=group)
        context['title'] = f"Участники группы: {group.name_of_group}"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


class GroupSettings(LoginRequiredMixin, DataMixin, ListView):
    """Страница настроек для админов"""
    model = Group
    template_name = 'groups/group_settings.html'
    context_object_name = 'group'

    def get_queryset(self):
        self.queryset = Group.objects.get(pk=self.kwargs['group_id'])
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.queryset
        members = GroupMember.objects.filter(group=group).select_related('member')
        context['members'] = members
        context['auth_user'] = members.get(member=self.request.user)
        context['group_banned'] = group.banned.all()
        context['title'] = f"Управление группой: {group.name_of_group}"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


class EditGroupView(LoginRequiredMixin, DataMixin, UpdateView):
    """Страница редактирования данных группы"""
    form_class = AddOrEditGroupForm
    template_name = 'groups/edit_group_page.html'

    def get_queryset(self):
        self.queryset = Group.objects.filter(pk=self.kwargs['pk'])
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование группы"
        context['auth_user'] = GroupMember.objects.get(
            member=self.request.user,
            group=self.queryset[0]
        )
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context

    def form_valid(self, form):
        form.save()
        return redirect('show_group', group_id=self.kwargs['pk'])


class DeleteGroup(LoginRequiredMixin, DataMixin, DeleteView):
    """Страница удаления группы"""
    model = Group
    template_name = 'groups/delete_group_page.html'

    def get_success_url(self):
        return reverse_lazy('my_groups')

    def get_queryset(self):
        qs = super(DeleteGroup, self).get_queryset()
        auth_user = GroupMember.objects.get(member=self.request.user, group=self.kwargs['pk'])

        return qs if auth_user.is_owner else None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Удаление группы"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


@login_required
def change_admin_to_group(request, group_id, admin_id):
    """Добавляет или удаляет админа в группу"""
    group = Group.objects.get(pk=group_id)
    auth_user = GroupMember.objects.get(member=request.user, group=group)
    user_change_status = GroupMember.objects.get(member__pk=admin_id, group=group)

    if auth_user.is_owner or (auth_user == user_change_status and user_change_status.is_admin):
        user_change_status.is_admin = False if user_change_status.is_admin else True
        user_change_status.save()

    return redirect('group_settings', group_id=group_id)


@login_required
def change_ban_to_user_in_group(request, group_id, user_id):
    """Даёт бан пользователю или снимает его"""
    group = Group.objects.get(pk=group_id)
    user = Owner.objects.get(pk=user_id)
    auth_user = GroupMember.objects.get(member=request.user, group=group)

    if auth_user.is_admin:
        user_member = GroupMember.objects.get(member=user, group=group)
        if auth_user.is_owner or not user_member.is_admin:
            if user in group.banned.all():
                group.banned.remove(user)
            else:
                group.banned.add(user)
                if user_member.is_admin:
                    user_member.is_admin = False
                    user_member.save()

    return redirect('group_settings', group_id=group_id)


@login_required
def change_owner_to_group(request, group_id, owner_id):
    """Меняет владельца группы"""
    group = Group.objects.get(pk=group_id)
    auth_user = GroupMember.objects.get(member=request.user, group=group)

    if auth_user.is_owner:
        new_owner = GroupMember.objects.get(member__pk=owner_id, group=group)
        new_owner.is_owner = new_owner.is_admin = True
        auth_user.is_owner = False
        new_owner.save()
        auth_user.save()

    return redirect('group_settings', group_id=group_id)
