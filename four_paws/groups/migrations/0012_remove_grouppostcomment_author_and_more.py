# Generated by Django 4.2.2 on 2023-09-30 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0011_alter_grouppost_options_remove_grouppost_date_create_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grouppostcomment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='grouppostcomment',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='grouppostcomment',
            name='post',
        ),
        migrations.RemoveField(
            model_name='grouppostimage',
            name='group',
        ),
        migrations.RemoveField(
            model_name='grouppostimage',
            name='post',
        ),
        migrations.DeleteModel(
            name='GroupPost',
        ),
        migrations.DeleteModel(
            name='GroupPostComment',
        ),
        migrations.DeleteModel(
            name='GroupPostImage',
        ),
    ]
