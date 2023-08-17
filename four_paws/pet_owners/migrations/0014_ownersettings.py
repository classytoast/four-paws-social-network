# Generated by Django 4.2.2 on 2023-08-17 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pet_owners', '0013_alter_animal_date_of_animal_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnerSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.BooleanField(default=False)),
                ('date_of_birth', models.BooleanField(default=False)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
