from django import template


register = template.Library()


@register.simple_tag
def create_foll_list(animal_name, user_animals_followed):
    """достает данные из словаря о подписчиках питомца"""
    return user_animals_followed[animal_name]


@register.simple_tag
def get_data_for_post(post_title, post_data):
    """достает данные из словаря для нужного поста"""
    return post_data[post_title]


@register.inclusion_tag('pet_owners/likes_and_views_for_posts.html')
def show_likes_and_views(post, post_data):
    return {"post": post, "post_data": post_data}
