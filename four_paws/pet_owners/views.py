from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.urls import reverse

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


def register(request):
    return render(request, 'pet_owners/register_page.html')


def login(request):
    return render(request, 'pet_owners/login_page.html')
