from django.db import models
from django.conf import settings

from pet_owners.models import Animal


class Group(models.Model):
    """Группа о домашних животных или теме касающехся их"""
    name_of_group = models.CharField(max_length=150, verbose_name='название группы')
    about_group = models.TextField(max_length=2000, verbose_name='инф о группе')
    img_of_group = models.ImageField(upload_to="img_of_group/%Y/%m/%d/", verbose_name='лого группы')
    date_create = models.DateField(auto_now_add=True, verbose_name='дата создания')

    def __str__(self):
        return self.name_of_group

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class GroupMember(models.Model):
    """Участник группы"""
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='group_subscriptions', verbose_name='участник')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='members', verbose_name='на что подписан')
    join_date = models.DateTimeField(auto_now_add=True, verbose_name='дата подписки')
    is_owner = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class GroupPost(models.Model):
    """пост в группе"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='группа')
    title = models.CharField(max_length=105, blank=True, verbose_name='заголовок')
    text_of_post = models.TextField(max_length=2000, verbose_name='текст поста')
    is_published = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания поста')
    views = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='grp_views', verbose_name='просмотры')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='grp_likes', verbose_name='лайки')

    def __str__(self):
        return f'{self.text_of_post}'[:15]

    class Meta:
        verbose_name = 'Пост пользователя'
        verbose_name_plural = 'Посты пользователей'


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
