from django import template


register = template.Library()


@register.simple_tag
def create_foll_list(animal_name, user_animals_followed):
    """достает данные из словаря о подписчиках питомца"""
    return user_animals_followed[animal_name]


@register.simple_tag
def get_img_for_post(post_title, imgs_for_posts):
    """достает изображение из словаря для нужного поста"""
    return imgs_for_posts[post_title]