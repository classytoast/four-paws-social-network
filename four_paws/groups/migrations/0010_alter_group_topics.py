# Generated by Django 4.2.2 on 2023-09-19 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0009_grouptopic_group_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='topics',
            field=models.ManyToManyField(blank=True, to='groups.grouptopic', verbose_name='тематики'),
        ),
    ]
