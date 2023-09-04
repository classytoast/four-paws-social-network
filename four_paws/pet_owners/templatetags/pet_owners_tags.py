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


@register.inclusion_tag('pet_owners/likes_and_views_for_posts.html')
def show_likes_and_views(post, post_data, name_page_for_likes, object_id):
    return {"post": post, "post_data": post_data,
            "name_page_for_likes": name_page_for_likes, "object_id": object_id}


@register.inclusion_tag('pet_owners/form_fields.html')
def show_form_fields(form):
    return {'form': form}


@register.inclusion_tag('pet_owners/all_posts.html')
def show_all_posts(posts, data_for_post, name_page_for_likes, object_id):
    return {"posts": posts, "data_for_post": data_for_post,
            "name_page_for_likes": name_page_for_likes, "object_id": object_id}


@register.simple_tag
def show_likes_for_comment(comment_pk, comment_likes):
    """достает данные о лайках из словаря для нужного комментария"""
    return comment_likes[str(comment_pk)]
