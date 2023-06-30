from django.db import models
from django.contrib.auth.models import User


class AnimalCategory(models.Model):
    """Вид домашнего животного"""
    category = models.CharField(max_length=255, verbose_name='вид домашнего животного')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Вид'
        verbose_name_plural = 'Виды'


class Owner(User):
    """Пользователь сайта"""
    date_of_birth = models.DateTimeField(blank=True, verbose_name='дата рождения пользователя')
    avatar = models.ImageField(upload_to="owners_photos/%Y/%m/%d/", blank=True, verbose_name='фото пользователя')
    date_of_registration = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации пользователя')
    about_myself = models.TextField(max_length=520, blank=True, verbose_name='о себе')
    instagram = models.URLField(blank=True, verbose_name='инстаграм')
    vkontakte = models.URLField(blank=True, verbose_name='вконтакте')
    youtube = models.URLField(blank=True, verbose_name='ютуб')


class Animal(models.Model):
    """Питомцец"""
    name_of_animal = models.CharField(max_length=55, verbose_name='имя питомца')
    pet_owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='владелец')
    category_of_animal = models.ForeignKey(AnimalCategory, on_delete=models.PROTECT, verbose_name='вид')
    animal_breed = models.CharField(max_length=100, blank=True, verbose_name='порода питомца')
    date_of_animal_birth = models.DateTimeField(verbose_name='дата рождения питомца')
    animal_photo = models.ImageField(upload_to="animals_photos/%Y/%m/%d/", verbose_name='фото питомца')
    about_pet = models.TextField(max_length=520, verbose_name='о питомце')

    def __str__(self):
        return self.name_of_animal

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'


class AnimalFollower(models.Model):
    """Подписчик животного"""
    follower = models.ForeignKey(Owner, on_delete=models.CASCADE,
                                 related_name='subscriptions', verbose_name='подписчик')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE,
                               related_name='followers', verbose_name='на кого подписан')
    join_date = models.DateTimeField(auto_now_add=True, verbose_name='дата подписки')


class OwnerPost(models.Model):
    """пост в блоге пользователя"""
    autor = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='автор поста')
    title = models.CharField(max_length=105, blank=True, verbose_name='заголовок')
    text_of_post = models.TextField(max_length=2000, verbose_name='текст поста')
    is_published = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания поста')
    views = models.FloatField(verbose_name='просмотры')
    likes = models.FloatField(verbose_name='лайки')

    def __str__(self):
        return f'{self.text_of_post}'[15]

    class Meta:
        verbose_name = 'Пост пользователя'
        verbose_name_plural = 'Посты пользователей'


class PostImage(models.Model):
    """изображение к посту"""
    img = models.ImageField(upload_to="img_of_post/%Y/%m/%d/", verbose_name='изображение')
    post = models.ForeignKey(OwnerPost, on_delete=models.CASCADE, related_name='images', verbose_name='пост')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='владелец фото')
    animals_on_img = models.ManyToManyField(Animal, blank=True, verbose_name='питомцы на фото')


class PostComment(models.Model):
    """комментарий к посту"""
    comment = models.TextField(max_length=550, verbose_name='комментарий')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата')
    post = models.ForeignKey(OwnerPost, on_delete=models.CASCADE, related_name='comments', verbose_name='пост')
    likes = models.FloatField(verbose_name='лайки')
    is_hidden = models.BooleanField(default=False, verbose_name='скрыт')
