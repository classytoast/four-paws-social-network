# Generated by Django 4.2.2 on 2023-08-22 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet_owners', '0015_owner_date_of_birth_is_hidden_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcomment',
            name='is_hidden',
        ),
    ]
