from django import template


register = template.Library()


@register.inclusion_tag('posts/all_posts.html')
def show_all_posts(posts, data_for_post, name_page_for_likes, object_id):
    return {"posts": posts, "data_for_post": data_for_post,
            "name_page_for_likes": name_page_for_likes, "object_id": object_id}


@register.simple_tag
def get_data_for_post(post_pk, post_data):
    """достает данные из словаря для нужного поста"""
    return post_data[str(post_pk)]


@register.inclusion_tag('posts/likes_and_views_for_posts.html')
def show_likes_and_views(post, post_data, name_page_for_likes, object_id):
    return {"post": post, "post_data": post_data,
            "name_page_for_likes": name_page_for_likes, "object_id": object_id}