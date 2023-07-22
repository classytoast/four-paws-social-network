from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required

from .forms import RegisterUserForm
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


def add_or_del_follower_for_animal(request, animal_id):
    """Добавляет или удаляет подписчика питомцу"""
    if request.user.is_authenticated:
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
    else:
        return redirect('login')


def put_or_remove_like_for_post(request, post_id):
    """Ставит или убирает лайк посту"""
    if request.user.is_authenticated:
        user = Owner.objects.get(pk=request.user.id)
        post = OwnerPost.objects.get(pk=post_id)
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
            post.views.add(user)
        return redirect('profile_home', id=post.autor.pk)
    else:
        return redirect('login')


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
        return redirect('home')


def login(request):
    return render(request, 'pet_owners/login_page.html')
