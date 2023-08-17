from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from pet_owners.utils import DataMixin
from pet_owners.models import OwnerPost, Owner, PostImage


class ShowPost(DataMixin, DetailView):
    """Страница отдельно взятого поста"""
    model = OwnerPost
    template_name = 'posts/post_page.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.model.objects.get(pk=self.kwargs['post_id'])
        user = Owner.objects.get(pk=post.autor.pk)
        context['title'] = post.title
        context.update(self.get_left_menu())
        all_posts = user.ownerpost_set.all()
        context['data_for_post'] = self.get_data_for_post(all_posts, all_images=True)
        self.add_one_view_for_post(post, user)
        return context


class CreatePostView(LoginRequiredMixin, DataMixin, CreateView):
    """Страница создания поста"""
    form_class = AddOrEditPostForm
    template_name = 'posts/add_post_page.html'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreatePostView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user_id'] = self.request.user.id
        return form_kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление поста"
        context.update(self.get_left_menu())
        return context

    def form_valid(self, form):
        form.instance.autor = self.request.user
        post = form.save()
        if 'add_photos' in self.request.POST:
            return redirect('add-images-to-post', post_id=post.pk)
        elif 'to_publish' in self.request.POST:
            return redirect('profile_home', id=self.request.user.id)


class AddImgsView(LoginRequiredMixin, DataMixin, CreateView):
    """Страница добавления изображений к посту"""
    form_class = AddImageForm
    template_name = 'posts/add_images.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление изображений"
        context.update(self.get_left_menu())
        post = OwnerPost.objects.get(pk=self.kwargs['post_id'])
        context['added_images'] = post.images.all()
        return context

    def form_valid(self, form):
        if form.instance.img:
            post = OwnerPost.objects.get(pk=self.kwargs['post_id'])
            if post.autor == self.request.user:
                form.instance.owner = self.request.user
                form.instance.post = post
                form.save()
        if 'add_more_photos' in self.request.POST:
            return redirect('add-images-to-post', post_id=self.kwargs['post_id'])
        elif 'to_publish' in self.request.POST:
            return redirect('profile_home', id=self.request.user.id)


class UpdatePostView(LoginRequiredMixin, DataMixin, UpdateView):
    """Страница редактирования поста"""
    form_class = AddOrEditPostForm
    template_name = 'posts/edit_post_page.html'

    def get_queryset(self):
        return OwnerPost.objects.filter(pk=self.kwargs['pk'],
                                        autor=self.request.user)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(UpdatePostView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user_id'] = self.request.user.id
        return form_kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование поста"
        context.update(self.get_left_menu())
        return context

    def form_valid(self, form):
        if 'cancel' in self.request.POST:
            return redirect('profile_home', id=self.request.user.id)
        post = form.save()
        if 'update_without_photos' in self.request.POST:
            return redirect('profile_home', id=self.request.user.id)
        elif 'update_with_photos' in self.request.POST:
            return redirect('add-images-to-post', post_id=post.pk)


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
        return context


@login_required
def delete_img(request, img_id):
    """Функция удаления изображения"""
    user = Owner.objects.get(pk=request.user.id)
    image = PostImage.objects.get(pk=img_id)
    post_id = image.post.pk
    if image.owner == user:
        image.delete()
    return redirect('add-images-to-post', post_id=post_id)

