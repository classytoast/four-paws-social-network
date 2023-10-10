from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from groups.models import Group
from .forms import *
from pet_owners.utils import DataMixin
from .models import Post, OwnerPost, PostImage
from comments.models import PostComment
from .utils import PostDataMixin


class ShowPost(PostDataMixin, DataMixin, DetailView):
    """Страница отдельно взятого поста"""
    model = Post
    template_name = 'posts/post_page.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.model.objects.get(pk=self.kwargs['post_id'])
        context['title'] = post.title if post.title else post.text_of_post[:10]
        context.update(self.get_left_menu())
        context.update(self.get_right_menu(self.request.user))
        self.check_user_saw_the_post(post, self.request.user)
        comments = PostComment.objects.filter(post=post)
        context['comments'] = comments
        context['data_for_posts'] = self.get_data_for_posts([post],
                                                            all_images=True,
                                                            type_of_posts=self.kwargs['type_of_post'],
                                                            comments=comments)
        context['likes_for_comments'] = self.get_likes_for_comments(comments, self.request.user)
        return context


class AbstractCreatePostView(LoginRequiredMixin, DataMixin, CreateView):
    """Страница создания абстрактного поста"""
    template_name = 'posts/add_post_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление поста"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


class CreateOwnerPostView(AbstractCreatePostView):
    """Страница создания поста пользователя"""
    form_class = AddOrEditOwnerPostForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreateOwnerPostView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user_id'] = self.request.user.id
        return form_kwargs

    def form_valid(self, form):
        post = Post.objects.create(author=self.request.user,
                                   title=form.data['title'],
                                   text_of_post=form.data['text_of_post'])
        OwnerPost.objects.create(post=post, animals=form.data['animals'])

        if 'add_photos' in self.request.POST:
            return redirect('add_images_to_post', post_id=post.pk,
                            type_of_post='owner_post')
        elif 'to_publish' in self.request.POST:
            return redirect('profile_home', id=self.request.user.id)


class CreateGroupPostView(AbstractCreatePostView):
    """Страница создания поста в группу"""
    form_class = AddOrEditGroupPostForm

    def form_valid(self, form):
        group = Group.objects.get(pk=self.kwargs['group_id'])
        post = Post.objects.create(author=self.request.user,
                                   title=form.data['title'],
                                   text_of_post=form.data['text_of_post'])
        GroupPost.objects.create(post=post, group=group)

        if 'add_photos' in self.request.POST:
            return redirect('add_images_to_post', post_id=post.pk,
                            type_of_post='group_post')
        elif 'to_publish' in self.request.POST:
            return redirect('show_group', group_id=self.kwargs['group_id'])


class AddImgsView(LoginRequiredMixin, DataMixin, CreateView):
    """Страница добавления изображений к посту"""
    form_class = AddImageForm
    template_name = 'posts/add_images.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление изображений"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        post = Post.objects.get(pk=self.kwargs['post_id'])
        context['added_images'] = post.images.all()
        return context

    def form_valid(self, form):
        if form.instance.img:
            post = Post.objects.get(pk=self.kwargs['post_id'])
            if post.author == self.request.user:
                form.instance.post = post
                form.save()

        if 'add_more_photos' in self.request.POST:
            return redirect('add_images_to_post', post_id=self.kwargs['post_id'],
                            type_of_post=self.kwargs['type_of_post'])
        elif 'to_publish' in self.request.POST:
            if self.kwargs['type_of_post'] == 'owner_post':
                return redirect('profile_home', id=self.request.user.id)
            elif self.kwargs['type_of_post'] == 'group_post':
                group_post = GroupPost.objects.get(post=post)
                return redirect('show_group', group_id=group_post.group.pk)


class AbstractUpdatePost(LoginRequiredMixin, DataMixin, UpdateView):
    template_name = 'posts/edit_post_page.html'

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование поста"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


class UpdateOwnerPostView(AbstractUpdatePost):
    """Страница редактирования поста"""
    form_class = AddOrEditOwnerPostForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(UpdateOwnerPostView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user_id'] = self.request.user.id
        return form_kwargs

    def form_valid(self, form):
        if 'cancel' in self.request.POST:
            return redirect('post', post_id=self.kwargs['pk'])

        post = Post.objects.get(pk=self.kwargs['pk'])
        owner_post = OwnerPost.objects.get(post=post)
        post.title, post.text_of_post = form.data['title'], form.data['text_of_post']
        owner_post.animals = form.data['animals']

        if 'update_without_photos' in self.request.POST:
            return redirect('post', post_id=self.kwargs['pk'])
        elif 'update_with_photos' in self.request.POST:
            return redirect('add_images_to_post', post_id=post.pk,
                            type_of_post='owner_post')


class UpdateGroupPostView(AbstractUpdatePost):
    """Страница редактирования поста в группе"""
    form_class = AddOrEditGroupPostForm

    def form_valid(self, form):
        if 'cancel' in self.request.POST:
            return redirect('post', post_id=self.kwargs['pk'])
        post = form.save()
        if 'update_without_photos' in self.request.POST:
            return redirect('post', post_id=self.kwargs['pk'])
        elif 'update_with_photos' in self.request.POST:
            return redirect('add_images_to_post', post_id=post.pk,
                            type_of_post='group_post')


class DeletePost(LoginRequiredMixin, DataMixin, DeleteView):
    """Страница удаления поста"""
    model = OwnerPost
    template_name = 'posts/delete_post_page.html'

    def get_success_url(self):
        return reverse_lazy('profile_home', kwargs={'id': self.request.user.id})

    def get_queryset(self):
        qs = super(DeletePost, self).get_queryset()
        return qs.filter(autor=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Удаление поста"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


@login_required
def delete_img(request, img_id):
    """Функция удаления изображения"""
    user = request.user
    image = PostImage.objects.get(pk=img_id)
    post = Post.objects.get(pk=image.post.pk)
    if post.author == user:
        image.delete()
    return redirect('add_images_to_post', post_id=post.pk)


