from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .utils import DataMixin
from .models import *


def index(request):
    return render(request, 'pet_owners/main_page.html')


class ProfileHome(DataMixin, ListView):
    """Страница профиля"""
    model = Owner
    template_name = 'pet_owners/profile_page.html'
    context_object_name = 'profile'
    all_animals = False

    def get_queryset(self):
        return Owner.objects.get(pk=self.kwargs['id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = Owner.objects.get(pk=self.kwargs['id'])
        if self.request.user.id == self.kwargs['id']:
            context['title'] = "Мой профиль"
        else:
            context['title'] = f"Профиль {user.username}"
        left_menu = self.get_left_menu()
        context.update(left_menu)
        subs_and_animals = self.get_subscriptions_and_animals_of_owner(user)
        context.update(subs_and_animals)
        owner_posts = self.get_owner_posts(user)
        context.update(owner_posts)
        return context


class ShowPost(DataMixin, DetailView):
    """Страница отдельно взятого поста"""
    model = OwnerPost
    template_name = 'pet_owners/post_page.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.model.objects.get(pk=self.kwargs['post_id'])
        user = Owner.objects.get(pk=post.autor.pk)
        context['title'] = post.title
        left_menu = self.get_left_menu()
        context.update(left_menu)
        owner_posts = self.get_owner_posts(user, all_images=True)
        context.update(owner_posts)
        self.add_one_view_for_post(post, user)
        return context


@login_required
def add_or_del_follower_for_animal(request, animal_id):
    """Добавляет или удаляет подписчика питомцу"""
    user = Owner.objects.get(pk=request.user.id)
    animal = Animal.objects.get(pk=animal_id)
    owner_id = animal.pet_owner.pk
    try:
        AnimalFollower.objects.get(follower=user,
                                   animal=animal
                                   ).delete()
    except AnimalFollower.DoesNotExist:
        AnimalFollower.objects.create(follower=user,
                                      animal=animal
                                      )
    return redirect('profile_home', id=owner_id)


@login_required
def put_or_remove_like_for_post(request, post_id):
    """Ставит или убирает лайк посту"""
    user = Owner.objects.get(pk=request.user.id)
    post = OwnerPost.objects.get(pk=post_id)
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        post.views.add(user)
    return redirect('profile_home', id=post.autor.pk)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'pet_owners/register_page.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        left_menu = self.get_left_menu()
        context.update(left_menu)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile_home', id=user.pk)


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'pet_owners/login_page.html'

    def get_success_url(self):
        return reverse_lazy('profile_home', kwargs={'id': self.request.user.id})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        left_menu = self.get_left_menu()
        context.update(left_menu)
        return context


def logout_user(request):
    logout(request)
    return redirect('login')


class CreatePostView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'pet_owners/add_post_page.html'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreatePostView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user_id'] = self.request.user.id
        return form_kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление поста"
        left_menu = self.get_left_menu()
        context.update(left_menu)
        return context

    def form_valid(self, form):
        form.instance.autor = self.request.user
        post = form.save()
        if 'add_photos' in self.request.POST:
            return redirect('add-images-to-post', post_id=post.pk)
        elif 'to_publish' in self.request.POST:
            return redirect('profile_home', id=self.request.user.id)


class AddImgsView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddImageForm
    template_name = 'pet_owners/add_images.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление изображений"
        left_menu = self.get_left_menu()
        context.update(left_menu)
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


@login_required
def delete_post(request, post_id):
    """Функция удаления поста"""
    user = Owner.objects.get(pk=request.user.id)
    post = OwnerPost.objects.get(pk=post_id)
    post_imgs = post.images.all()
    if post.autor == user:
        post.delete()
        post_imgs.delete()
    return redirect('profile_home', id=request.user.id)
