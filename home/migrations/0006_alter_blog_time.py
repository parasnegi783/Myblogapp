# Generated by Django 5.1 on 2024-08-29 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_blog_thumbnail_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='time',
            field=models.DateField(),
        ),
    ]
