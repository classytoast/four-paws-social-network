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
        if kwargs['is_authenticated']:
            aut_user = Owner.objects.get(pk=kwargs['id'])
            context['left_menu'] = _create_left_menu(aut_user)
        else:
            context['left_menu'] = _create_left_menu(is_authenticated=False)
        return context