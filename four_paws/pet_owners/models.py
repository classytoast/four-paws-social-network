from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


class AnimalCategory(models.Model):
    """Вид домашнего животного"""
    category = models.CharField(max_length=255, verbose_name='вид домашнего животного')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Вид'
        verbose_name_plural = 'Виды'


class Owner(AbstractUser):
    """Пользователь сайта"""
    date_of_birth = models.DateField(blank=True, verbose_name='дата рождения пользователя', null=True)
    avatar = models.ImageField(upload_to="owners_photos/%Y/%m/%d/", blank=True,
                               verbose_name='фото пользователя', null=True)
    about_myself = models.TextField(max_length=520, blank=True, verbose_name='о себе', null=True)
    instagram = models.URLField(blank=True, verbose_name='инстаграм', null=True)
    vkontakte = models.URLField(blank=True, verbose_name='вконтакте', null=True)
    youtube = models.URLField(blank=True, verbose_name='ютуб', null=True)

    def get_absolute_url(self):
        """создание ссылки на страницу профиля"""
        return reverse('profile_home', kwargs={'id': self.pk})

    def get_absolute_url_with_all_animals(self):
        """создание ссылки на страницу профиля,
        с отображением всех животных
        """
        return reverse('profile_with_all_animals', kwargs={'id': self.pk})


class Animal(models.Model):
    """Питомцец"""
    GENDER = (
        ("male", "male"),
        ("female", "female")
    )
    name_of_animal = models.CharField(max_length=55, verbose_name='имя питомца')
    pet_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')
    category_of_animal = models.ForeignKey(AnimalCategory, on_delete=models.PROTECT, verbose_name='вид')
    animal_breed = models.CharField(max_length=100, blank=True, verbose_name='порода питомца')
    date_of_animal_birth = models.DateField(verbose_name='дата рождения питомца')
    sex = models.CharField(max_length=6, choices=GENDER, verbose_name='пол', null=True)
    animal_photo = models.ImageField(upload_to="animals_photos/%Y/%m/%d/", verbose_name='фото питомца')
    about_pet = models.TextField(max_length=520, verbose_name='о питомце')

    def __str__(self):
        return self.name_of_animal

    def change_follower(self):
        """добавление подписчика питомцу"""
        return reverse('change_follower_for_animal', kwargs={'animal_id': self.pk})

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'


class AnimalFollower(models.Model):
    """Подписчик животного"""
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='subscriptions', verbose_name='подписчик')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE,
                               related_name='followers', verbose_name='на кого подписан')
    join_date = models.DateField(auto_now_add=True, verbose_name='дата подписки')

    class Meta:
        verbose_name = 'Подписчик питомца'
        verbose_name_plural = 'Подписчики питомцев'


class OwnerPost(models.Model):
    """пост в блоге пользователя"""
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='автор поста')
    title = models.CharField(max_length=105, blank=True, verbose_name='заголовок')
    text_of_post = models.TextField(max_length=2000, verbose_name='текст поста')
    animals = models.ManyToManyField(Animal, related_name='posts',
                                     verbose_name='питомцы в посте')
    is_published = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания поста')
    views = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='views', verbose_name='просмотры')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', verbose_name='лайки')

    def __str__(self):
        return f'{self.text_of_post}'[:15]

    class Meta:
        verbose_name = 'Пост пользователя'
        verbose_name_plural = 'Посты пользователей'
        ordering = ['-date_create']


class PostImage(models.Model):
    """изображение к посту"""
    img = models.ImageField(upload_to="img_of_post/%Y/%m/%d/", verbose_name='изображение')
    post = models.ForeignKey(OwnerPost, on_delete=models.CASCADE, related_name='images', verbose_name='пост')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец фото')


class PostComment(models.Model):
    """комментарий к посту"""
    comment = models.TextField(max_length=550, verbose_name='комментарий')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата')
    post = models.ForeignKey(OwnerPost, on_delete=models.CASCADE, related_name='comments', verbose_name='пост')
    likes = models.FloatField(verbose_name='лайки')
    is_hidden = models.BooleanField(default=False, verbose_name='скрыт')
