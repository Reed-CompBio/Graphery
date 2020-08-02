# Generated by Django 3.0.7 on 2020-07-05 21:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20200705_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enusgraph',
            name='authors',
        ),
        migrations.RemoveField(
            model_name='zhcngraph',
            name='authors',
        ),
        migrations.AddField(
            model_name='graph',
            name='authors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
