from django import template


register = template.Library()


@register.simple_tag
def create_foll_list(animal_name, user_animals_followed):
    """достает данные из словаря о подписчиках питомца"""
    return user_animals_followed[animal_name]


@register.simple_tag
def create_range(start, finish):
    """Решает проблему с точкой для range в шаблоне"""
    return range(start, finish)


@register.simple_tag
def get_object_on_index(array, index):
    try:
        return array[index]
    except IndexError:
        return None


@register.inclusion_tag('pet_owners/form_fields.html')
def show_form_fields(form):
    return {'form': form}


@register.simple_tag
def show_likes_for_comment(comment_pk, comment_likes):
    """достает данные о лайках из словаря для нужного комментария"""
    return comment_likes[str(comment_pk)]
