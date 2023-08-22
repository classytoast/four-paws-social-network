from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout, login
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from .forms import *
from .utils import DataMixin
from .models import *


@login_required
def index(request):
    """При входе на сайт, пользователя сразу перенаправляет
    на его страницу, если он залогинен"""
    return redirect('profile_home', id=request.user.id)


class ProfileHome(LoginRequiredMixin, DataMixin, ListView):
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
        all_posts = owner.ownerpost_set.all()
        context['all_posts'] = all_posts
        context['data_for_post'] = self.get_data_for_post(all_posts)
        context['name_page_for_likes'] = 'owner_posts'
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
def put_or_remove_like_for_post(request, post_id, from_page):
    """Ставит или убирает лайк посту"""
    user = Owner.objects.get(pk=request.user.id)
    post = OwnerPost.objects.get(pk=post_id)
    print('sffsdfsd', from_page)
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        post.views.add(user)
    if from_page == 'post_detail':
        return redirect('post', post_id=post_id)
    elif from_page == 'owner_posts':
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
        context['auth_user'] = Owner.objects.get(pk=self.request.user.id)
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
    """Cтраница регистрации пользователей"""
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
    """Страница авторизации пользователей"""
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
    """Выход из учетной записи"""
    logout(request)
    return redirect('login')


class UpdateOwner(LoginRequiredMixin, DataMixin, UpdateView):
    """Страница редактирования данных о пользователе"""
    form_class = UpdateUserForm
    template_name = 'pet_owners/edit_owner_page.html'

    def get_queryset(self):
        return Owner.objects.filter(pk=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование профиля"
        context.update(self.get_left_menu())
        return context

    def form_valid(self, form):
        form.save()
        return redirect('profile_home', id=self.request.user.id)


class PrivacySettingsView(LoginRequiredMixin, DataMixin, UpdateView):
    """Страница настроек приватности"""
    form_class = PrivacySettingsForm
    template_name = 'pet_owners/privacy_settings_page.html'

    def get_queryset(self):
        return Owner.objects.filter(pk=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Настройки приватности"
        context.update(self.get_left_menu())
        return context

    def form_valid(self, form):
        form.save()
        return redirect('profile_home', id=self.request.user.id)


class ChangePasswordView(LoginRequiredMixin, DataMixin, PasswordChangeView):
    """Страница изменения пароля"""
    form_class = NewPasswordForm
    template_name = 'pet_owners/change_password_page.html'

    def get_success_url(self):
        return reverse_lazy('profile_home', kwargs={'id': self.request.user.id})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Изменение пароля"
        context.update(self.get_left_menu())
        return context

