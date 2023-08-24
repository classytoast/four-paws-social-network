from .models import *


class DataMixin:
    """Общий класс для всех вьюшек"""

    def get_left_menu(self):
        """Создает список ссылок для левой панели меню"""
        context = {}
        if self.request.user.is_authenticated:
            context['left_menu'] = [
                {'title': "Мой профиль", 'url_name': ['profile_home', self.request.user.id]},
                {'title': "Мои питомцы", 'url_name': ['all_animals_page']},
                {'title': "Подписки", 'url_name': ['owner_subscriptions', self.request.user.id]},
                {'title': "Группы", 'url_name': ['profile_home', self.request.user.id]},
                {'title': "Найти...", 'url_name': ['profile_home', self.request.user.id]}
            ]
        else:
            context['left_menu'] = [
                {'title': "Регистрация", 'url_name': 'register'},
                {'title': "Войти", 'url_name': 'login'},
            ]
        return context

    def get_right_menu(self, auth_user=None):
        """Создает список ссылок для правой панели меню"""
        context = {}
        if auth_user is None:
            auth_user = Owner.objects.get(pk=self.request.user.id)
        animals = Animal.objects.filter(followers__follower=auth_user)[:7]
        context['animals_for_right_menu'] = animals
        return context

    def get_animals_followers_of_owner(self, animals):
        """Выдает подписчиков питомцев юзера"""
        user_animals_followed = {}
        for animal in animals:
            animal_folls = animal.followers.all()
            count_folls = animal_folls.count()
            try:
                animal_folls.get(follower__id=self.request.user.id)
                user_animals_followed[f'{animal.name_of_animal}'] = {"is_followed": True,
                                                                     "count_folls": count_folls
                                                                     }
            except AnimalFollower.DoesNotExist:
                user_animals_followed[f'{animal.name_of_animal}'] = {"is_followed": False,
                                                                     "count_folls": count_folls
                                                                     }
        return user_animals_followed

    def get_data_for_post(self, posts, auth_user, all_images=False):
        """Выгружает данные для переданных постов"""
        data_for_post = {}
        for post in posts:
            if self.request.user.is_authenticated and auth_user in post.likes.all():
                is_liked = True
            else:
                is_liked = False
            if all_images:
                data_for_post[f'{post.title}'] = {
                    'img': post.images.all(),
                    'is_liked': is_liked
                }
            else:
                data_for_post[f'{post.title}'] = {
                    'img': post.images.first(),
                    'is_liked': is_liked
                }
        return data_for_post

    def add_one_view_for_post(self, post, user):
        """Добавляет просмотр посту"""
        if self.request.user.is_authenticated and user not in post.likes.all():
            post.views.add(user)

    def get_likes_for_comments(self, comments):
        """Выгружает данные о лайках для переданных комментариев"""
        likes_for_comment = {}
        auth_user = Owner.objects.get(pk=self.request.user.id)
        for comment in comments:
            if self.request.user.is_authenticated and auth_user in comment.likes.all():
                likes_for_comment[f'{comment.pk}'] = True
            else:
                likes_for_comment[f'{comment.pk}'] = False
        return likes_for_comment

