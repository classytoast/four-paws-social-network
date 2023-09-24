from groups.models import GroupPostComment
from pet_owners.models import PostComment, OwnerPost


class PostDataMixin:
    """Миксин работы с данными для постов"""

    def get_data_for_posts(self, posts, type_of_post, all_images=False):
        """Выгружает необходимые для отображения данные переданных постов"""
        data_for_posts = {}
        auth_user = self.request.user

        for post in posts:
            data_for_posts[f'{post.title}'] = {}

            if auth_user.is_authenticated and auth_user in post.likes.all():
                data_for_posts[f'{post.title}']['is_liked'] = True
            else:
                data_for_posts[f'{post.title}']['is_liked'] = False

            data_for_posts[f'{post.title}']['img'] = post.images.all() if all_images else post.images.first()

            if type_of_post == 'owner-post':
                data_for_posts[f'{post.title}']['animals'] = OwnerPost.objects.get(post=post).animals.all()
                data_for_posts[f'{post.title}']['comments_count'] = PostComment.objects.filter(post=post).count()
                is_admin = True if post.author == auth_user else False
            elif type_of_post == 'group-post':
                data_for_posts[f'{post.title}']['comments_count'] = GroupPostComment.objects.filter(post=post).count()
                is_admin = True if post_is_in_group['is_admin'] else False

        return data_for_posts
