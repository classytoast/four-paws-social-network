# Generated by Django 4.2.2 on 2023-07-27 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_owners', '0010_remove_ownerpost_likes_remove_ownerpost_views_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='sex',
            field=models.CharField(choices=[('мальчик', 'мальчик'), ('девочка', 'девочка')], max_length=7, null=True, verbose_name='пол'),
        ),
    ]
