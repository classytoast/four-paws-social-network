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
def show_likes_and_views(post, post_data, name_page_for_likes):
    return {"post": post, "post_data": post_data,
            "name_page_for_likes": name_page_for_likes}


@register.inclusion_tag('pet_owners/form_fields.html')
def show_form_fields(form):
    return {'form': form}


@register.inclusion_tag('pet_owners/all_posts.html')
def show_all_posts(posts, data_for_post, name_page_for_likes):
    return {"posts": posts, "data_for_post": data_for_post,
            "name_page_for_likes": name_page_for_likes}
