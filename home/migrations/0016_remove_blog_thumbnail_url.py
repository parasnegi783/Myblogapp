# Generated by Django 5.1 on 2024-08-30 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_blog_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='thumbnail_url',
        ),
    ]
