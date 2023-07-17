# Generated by Django 4.2.2 on 2023-07-17 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_owners', '0005_alter_animal_date_of_animal_birth_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animalfollower',
            options={'verbose_name': 'Подписчик питомца', 'verbose_name_plural': 'Подписчики питомцев'},
        ),
        migrations.AddField(
            model_name='ownerpost',
            name='animals',
            field=models.ManyToManyField(null=True, related_name='posts', to='pet_owners.animal', verbose_name='питомцы в посте'),
        ),
    ]
