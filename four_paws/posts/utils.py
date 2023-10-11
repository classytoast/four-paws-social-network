from groups.models import GroupMember
from .models import OwnerPost, GroupPost
from comments.models import PostComment


class PostDataMixin:
    """Миксин работы с данными для постов"""

    def get_data_for_posts(self,
                           posts: list[object],
                           type_of_posts: str,
                           all_images: bool = False,
                           comments: object = None) -> dict:
        """
        Выгрузить необходимые для отображения данные переданных постов
        :param posts: список постов
        :param type_of_posts: тип постов (напр. в группе или на странице юзера)
        :param all_images: параметр, указывающий сколько фотографий нужно выгружать для каждого поста
        (все или один)
        :param comments: комментарии, количество которых необходимо вычислить
        :return: словарь, ключами которого являются заголовки постов, а значениями - выгруженные данные
        """
        data_for_posts = {}

        for post in posts:
            data_for_posts[f'{post.pk}'] = {}

            if self.request.user.is_authenticated and self.request.user in post.likes.all():
                data_for_posts[f'{post.pk}']['is_liked'] = True
            else:
                data_for_posts[f'{post.pk}']['is_liked'] = False

            data_for_posts[f'{post.pk}']['img'] = post.images.all() if all_images \
                else post.images.first()

            if type_of_posts == 'owner_post':
                owner_post = OwnerPost.objects.get(post=post)
                data_for_posts[f'{post.pk}'].update(self.get_data_for_owner_post(post, owner_post))

            elif type_of_posts == 'group_post':
                group_post = GroupPost.objects.get(post=post)
                data_for_posts[f'{post.pk}'].update(self.get_data_for_group_post(group_post))

            if comments is None:
                data_for_posts[f'{post.pk}']['comments_count'] = PostComment.objects.filter(post=post).count()
            else:
                data_for_posts[f'{post.pk}']['comments_count'] = comments.count()

        return data_for_posts

    def get_data_for_owner_post(self, post: object, owner_post: object) -> dict:
        """Выгрузить данные для поста юзера"""
        return {'animals': owner_post.animals.all(),
                'is_admin': True if self.request.user.is_authenticated and post.author == self.request.user else False}

    def get_data_for_group_post(self, group_post: object) -> dict:
        """Выгрузить данные для поста группы"""
        try:
            GroupMember.objects.get(group=group_post.group, member=self.request.user, is_admin=True)
            is_admin = True
        except GroupMember.DoesNotExist:
            is_admin = False
        return {'is_admin': is_admin}

    def check_user_saw_the_post(self, post, user):
        """Добавляет просмотр посту"""
        if self.request.user.is_authenticated and user not in post.views.all():
            post.views.add(user)
