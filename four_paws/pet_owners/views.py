from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required

from .forms import *
from .utils import DataMixin
from .models import *


@login_required
def index(request):
    """При входе на сайт, пользователя сразу перенаправляет
    на его страницу, если он залогинен"""
    return redirect('profile_home', id=request.user.id)


class ProfileHome(DataMixin, ListView):
    """Страница профиля"""
    model = Owner
    template_name = 'pet_owners/profile_page.html'
    context_object_name = 'profile'
    all_animals = False

    def get_queryset(self):
        self.queryset = Owner.objects.get(pk=self.kwargs['id'])
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.queryset
        animals = owner.animal_set.annotate(foll_count=Count('followers')).order_by('-foll_count')
        context['num_of_animals'] = animals.count()
        if self.all_animals:
            context['all_animals'] = True
            context['animals'] = animals
        else:
            context['all_animals'] = False
            context['animals'] = animals[:4]
        if self.request.user.id == self.kwargs['id']:
            context['title'] = "Мой профиль"
        else:
            context['title'] = f"Профиль {owner.username}"
        context.update(self.get_left_menu())
        subscriptions = owner.subscriptions.all()
        context['num_of_subs'] = subscriptions.count()
        context['user_animals_followed'] = self.get_animals_followers_of_owner(animals)
        context.update(self.get_owner_posts(owner))
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


class OwnerSubscriptions(DataMixin, ListView):
    """Страница подписок юзера"""
    model = Owner
    template_name = 'pet_owners/subscriptions_page.html'
    context_object_name = 'profile'

    def get_queryset(self):
        self.queryset = Owner.objects.get(pk=self.kwargs['id'])
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.queryset
        animals = Animal.objects.filter(followers__follower=owner)
        context['subscriptions'] = animals
        if self.request.user.id == self.kwargs['id']:
            context['title'] = "Мои подписки"
        else:
            context['title'] = f"Подписки {owner.username}"
        context.update(self.get_left_menu())
        context['user_animals_followed'] = self.get_animals_followers_of_owner(animals)
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'pet_owners/register_page.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        context.update(self.get_left_menu())
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
        context.update(self.get_left_menu())
        return context


def logout_user(request):
    logout(request)
    return redirect('login')
