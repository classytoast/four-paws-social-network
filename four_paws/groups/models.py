from django.db import models
from four_paws import settings


class GroupTopic(models.Model):
    """Класс для тематик в группах"""
    name = models.CharField(max_length=55, verbose_name='название')

    def __str__(self):
        return self.name


class Group(models.Model):
    """Группа о домашних животных или теме касающехся их"""
    name_of_group = models.CharField(max_length=150, verbose_name='название группы')
    about_group = models.TextField(max_length=2000, verbose_name='инф о группе')
    img_of_group = models.ImageField(upload_to="img_of_group/%Y/%m/%d/", verbose_name='лого группы')
    date_create = models.DateField(auto_now_add=True, verbose_name='дата создания')
    banned = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='banned_in_group', verbose_name='забаненные')
    topics = models.ManyToManyField(GroupTopic, blank=True, verbose_name='тематики')

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

