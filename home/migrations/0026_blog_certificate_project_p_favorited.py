# Generated by Django 5.1 on 2024-09-09 08:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_blog_favorited_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='certificate',
            field=models.FileField(blank=True, null=True, upload_to='certificates/'),
        ),
        migrations.AddField(
            model_name='project',
            name='P_favorited',
            field=models.ManyToManyField(blank=True, related_name='P_favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
