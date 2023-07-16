from django import template


register = template.Library()


@register.simple_tag
def create_foll_list(animal_name, user_animals_followed):
    """достает данные из словаря о подписчиках питомца,
    где ключем является имя питомца, а значение состоит из
    из данных: подписан ли пользователь на питомца,
    и сколько всего у питомца подписчиков"""
    return user_animals_followed[animal_name]

