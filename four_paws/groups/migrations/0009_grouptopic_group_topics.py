# Generated by Django 4.2.2 on 2023-09-19 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_group_banned'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='название')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='topics',
            field=models.ManyToManyField(blank=True, null=True, to='groups.grouptopic', verbose_name='тематики'),
        ),
    ]
