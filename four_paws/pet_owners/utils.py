from django.db.models import Count

from .models import *


def _create_left_menu(user=None, is_authenticated=True):
    if is_authenticated:
        left_menu = [
            {'title': "Мой профиль", 'url_name': ['profile_home', user.pk]},
            {'title': "Мои питомцы", 'url_name': ['profile_home', user.pk]},
            {'title': "Подписки", 'url_name': ['profile_home', user.pk]},
            {'title': "Подписчики", 'url_name': ['profile_home', user.pk]},
            {'title': "Группы", 'url_name': ['profile_home', user.pk]},
        ]
    else:
        left_menu = [
            {'title': "Регистрация", 'url_name': 'register'},
            {'title': "Войти", 'url_name': 'login'},
        ]
    return left_menu


class DataMixin:
    """Общий класс для всех вьюшек"""

    def get_user_context(self, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated:
            user = Owner.objects.get(pk=self.request.user.id)
            context['left_menu'] = _create_left_menu(user)
        else:
            context['left_menu'] = _create_left_menu(is_authenticated=False)
        return context

    def get_subscriptions_and_animals_of_owner(self, profile_id):
        """Выдает количество подписок юзера, его питомцев
        и их подписчиков
        """
        context = {}
        user = Owner.objects.get(pk=profile_id)
        subscriptions = user.subscriptions.all()
        context['num_of_subs'] = subscriptions.count()
        animals = user.animal_set.annotate(foll_count=Count('followers')).order_by('-foll_count')
        context['num_of_animals'] = animals.count()
        if self.all_animals:
            context['all_animals'] = True
            context['animals'] = animals
        else:
            context['all_animals'] = False
            context['animals'] = animals[:4]
        user_animals_followed = {}
        for animal in animals:
            animal_folls = animal.followers.all()
            count_folls = animal_folls.count()
            try:
                animal_folls.get(follower__id=self.request.user.id)
                user_animals_followed[f'{animal.name_of_animal}'] = [True, count_folls]
            except AnimalFollower.DoesNotExist:
                user_animals_followed[f'{animal.name_of_animal}'] = [False, count_folls]
        context['user_animals_followed'] = user_animals_followed
        return context

