# Generated by Django 4.2.2 on 2023-10-02 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_grouppost_ownerpost_postcomment_ownerpostimage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcomment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='postcomment',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='postcomment',
            name='post',
        ),
        migrations.DeleteModel(
            name='GroupPostComment',
        ),
        migrations.DeleteModel(
            name='PostComment',
        ),
    ]