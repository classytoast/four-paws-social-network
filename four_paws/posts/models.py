from django.db import models

from four_paws import settings
from groups.models import Group
from pet_owners.models import Animal


class Post(models.Model):
    """Модель стандартного поста"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='автор поста')
    title = models.CharField(max_length=105, blank=True, verbose_name='заголовок')
    text_of_post = models.TextField(max_length=2000, verbose_name='текст поста')
    is_published = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания поста')
    views = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='views', verbose_name='просмотры')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', verbose_name='лайки')

    def __str__(self):
        return f'{self.text_of_post}'[:15]

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_create']


class OwnerPost(models.Model):
    """пост в блоге пользователя"""
    post = models.OneToOneField(Post, on_delete=models.CASCADE, null=True, verbose_name='пост')
    animals = models.ManyToManyField(Animal, related_name='posts',
                                     verbose_name='питомцы в посте')

    def __str__(self):
        return f'{self.post}'[:15]

    class Meta:
        verbose_name = 'Пост пользователя'
        verbose_name_plural = 'Посты пользователей'


class OwnerPostImage(models.Model):
    """изображение к посту"""
    img = models.ImageField(upload_to="img_of_post/%Y/%m/%d/", verbose_name='изображение')
    post = models.ForeignKey(OwnerPost, on_delete=models.CASCADE, related_name='images', verbose_name='пост')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец фото')


class PostComment(models.Model):
    """комментарий к посту"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments',
                               on_delete=models.CASCADE, verbose_name='автор комментария', null=True)
    comment = models.TextField(max_length=550, verbose_name='комментарий')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата')
    post = models.ForeignKey(OwnerPost, on_delete=models.CASCADE, related_name='comments', verbose_name='пост')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comments_likes', verbose_name='лайки')


class GroupPost(models.Model):
    """пост в группе"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='группа')
    post = models.OneToOneField(Post, on_delete=models.CASCADE, null=True, verbose_name='пост')

    def __str__(self):
        return f'{self.post}'[:15]

    class Meta:
        verbose_name = 'Пост в группе'
        verbose_name_plural = 'Посты в группах'


class GroupPostImage(models.Model):
    """изображение к посту в группе"""
    img = models.ImageField(upload_to="img_of_post/%Y/%m/%d/", verbose_name='изображение')
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='images', verbose_name='пост')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='группа')


class GroupPostComment(models.Model):
    """комментарий к посту в группе"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='group_comments',
                               on_delete=models.CASCADE, verbose_name='автор комментария', null=True)
    comment = models.TextField(max_length=550, verbose_name='комментарий')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата')
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='comments', verbose_name='пост')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='group_comments_likes', verbose_name='лайки')