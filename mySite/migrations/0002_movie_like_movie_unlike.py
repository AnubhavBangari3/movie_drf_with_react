# Generated by Django 4.0.6 on 2022-08-24 14:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mySite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movie',
            name='unlike',
            field=models.ManyToManyField(blank=True, related_name='unlike', to=settings.AUTH_USER_MODEL),
        ),
    ]