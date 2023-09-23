# Generated by Django 4.2.2 on 2023-09-23 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        ('pet_owners', '0019_alter_postcomment_author'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostImage',
            new_name='OwnerPostImage',
        ),
        migrations.AlterModelOptions(
            name='ownerpost',
            options={'verbose_name': 'Пост пользователя', 'verbose_name_plural': 'Посты пользователей'},
        ),
        migrations.RemoveField(
            model_name='ownerpost',
            name='autor',
        ),
        migrations.RemoveField(
            model_name='ownerpost',
            name='date_create',
        ),
        migrations.RemoveField(
            model_name='ownerpost',
            name='is_published',
        ),
        migrations.RemoveField(
            model_name='ownerpost',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='ownerpost',
            name='text_of_post',
        ),
        migrations.RemoveField(
            model_name='ownerpost',
            name='title',
        ),
        migrations.RemoveField(
            model_name='ownerpost',
            name='views',
        ),
        migrations.AddField(
            model_name='ownerpost',
            name='post',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='пост'),
        ),
    ]
