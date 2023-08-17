# Generated by Django 4.2.2 on 2023-08-17 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_owners', '0014_ownersettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='date_of_birth_is_hidden',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='owner',
            name='full_name_is_hidden',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='OwnerSettings',
        ),
    ]