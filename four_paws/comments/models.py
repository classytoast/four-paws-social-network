from django.db import models

from four_paws import settings
from posts.models import Post


class PostComment(models.Model):
    """комментарий к посту"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments',
                               on_delete=models.CASCADE, verbose_name='автор комментария', null=True)
    comment = models.TextField(max_length=550, verbose_name='комментарий')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='пост')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comments_likes', verbose_name='лайки')
