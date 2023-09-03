from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
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
        all_posts = GroupPost.objects.filter(group=group)
        context['all_posts'] = all_posts
        auth_user = self.request.user
        context['user_groups_followed'] = self.get_groups_followers([group])
        context['data_for_post'] = self.get_data_for_post(
            all_posts,
            auth_user,
            post_is_in_group={
                "is_admin": context['user_groups_followed'][group.name_of_group]['is_admin']
            }
        )
        context.update(self.get_left_menu())
        context.update(self.get_right_menu(auth_user))
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


class ShowGroupPost(DataMixin, DetailView):
    """Страница отдельно взятого поста в группе"""
    model = GroupPost
    template_name = 'groups/group_post_page.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.model.objects.get(pk=self.kwargs['post_id'])
        context['title'] = post.title
        context.update(self.get_left_menu())
        auth_user = self.request.user
        context.update(self.get_right_menu(auth_user))
        context['data_for_post'] = self.get_data_for_post(
            [post],
            auth_user,
            post_is_in_group={"is_admin": False},
            all_images=True
        )
        self.add_one_view_for_post(post, auth_user)
        comments = GroupPostComment.objects.filter(post=post)
        context['comments'] = comments
        context['likes_for_comments'] = self.get_likes_for_comments(comments, auth_user)
        return context


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
        form.instance.group = Group.objects.get(pk=self.kwargs['group_id'])
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
    template_name = 'groups/add_images.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление изображений"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        post = GroupPost.objects.get(pk=self.kwargs['post_id'])
        context['group_id'] = self.kwargs['group_id']
        context['added_images'] = post.images.all()
        return context

    def form_valid(self, form):
        if form.instance.img:
            post = GroupPost.objects.get(pk=self.kwargs['post_id'])
            form.instance.group = post.group
            form.instance.post = post
            form.save()
        if 'add_more_photos' in self.request.POST:
            return redirect('add_images_to_group_post',
                            group_id=self.kwargs['group_id'],
                            post_id=self.kwargs['post_id'])
        elif 'to_publish' in self.request.POST:
            return redirect('show_group', group_id=self.kwargs['group_id'])


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Удаление поста в группе"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


@login_required
def delete_img_for_group_post(request, group_id, img_id):
    """Функция удаления изображения"""
    image = GroupPostImage.objects.get(pk=img_id)
    post = image.post
    image.delete()
    return redirect('add_images_to_group_post', group_id=group_id, post_id=post.pk)
