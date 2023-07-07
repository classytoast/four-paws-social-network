from .models import *


left_menu = [{'title': "Мой профиль", 'url_name': 'profile_home'},
             {'title': "Мои питомцы", 'url_name': 'profile_home'},
             {'title': "Подписки", 'url_name': 'profile_home'},
             {'title': "Подписчики", 'url_name': 'profile_home'},
             {'title': "Группы", 'url_name': 'profile_home'},
        ]


class DataMixin:
    """Общий класс для всех вьюшек"""

    def get_user_context(self, **kwargs):
        context = kwargs
        context['left_menu'] = left_menu
        return context