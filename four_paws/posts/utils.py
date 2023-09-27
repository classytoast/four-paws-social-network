from groups.models import GroupPostComment, GroupMember, GroupPost
from pet_owners.models import PostComment, OwnerPost


class PostDataMixin:
    """Миксин работы с данными для постов"""

    def get_data_for_posts(self, posts: list[object], type_of_posts: str,
                           all_images: bool = False) -> dict:
        """
        Выгрузить необходимые для отображения данные переданных постов
        :param posts: список постов
        :param type_of_posts: тип постов (напр. в группе или на странице юзера)
        :param all_images: параметр, указывающий сколько фотографий нужно выгружать для каждого поста
        (все или один)
        :return: словарь, ключами которого являются заголовки постов, а значениями - выгруженные данные
        """
        data_for_posts = {}

        for post in posts:
            data_for_posts[f'{post.title}'] = {}

            if self.request.user.is_authenticated and self.request.user in post.likes.all():
                data_for_posts[f'{post.title}']['is_liked'] = True
            else:
                data_for_posts[f'{post.title}']['is_liked'] = False

            data_for_posts[f'{post.title}']['img'] = post.images.all() if all_images else post.images.first()

            if type_of_posts == 'owner-post':
                data_for_posts[f'{post.title}'].update(self.get_data_for_owner_post(post))
            elif type_of_posts == 'group-post':
                data_for_posts[f'{post.title}'].update(self.get_data_for_group_post(post))

        return data_for_posts

    def get_data_for_owner_post(self, post: object) -> dict:
        """Выгрузить данные для поста юзера"""
        return {'animals': OwnerPost.objects.get(post=post).animals.all(),
                'comments_count': PostComment.objects.filter(post=post).count(),
                'is_admin': True if post.author == self.request.user else False}

    def get_data_for_group_post(self, post: object) -> dict:
        """Выгрузить данные для поста группы"""
        admins = GroupMember.objects.filter(group=GroupPost.objects.get(post=post), is_admin=True)
        return {'comments_count': GroupPostComment.objects.filter(post=post).count(),
                'is_admin': True if self.request.user in admins else False}
