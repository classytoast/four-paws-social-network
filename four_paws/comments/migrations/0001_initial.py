# Generated by Django 4.2.2 on 2023-10-02 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0003_remove_postcomment_author_remove_postcomment_likes_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=550, verbose_name='комментарий')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='дата')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='автор комментария')),
                ('likes', models.ManyToManyField(related_name='comments_likes', to=settings.AUTH_USER_MODEL, verbose_name='лайки')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post', verbose_name='пост')),
            ],
        ),
    ]
