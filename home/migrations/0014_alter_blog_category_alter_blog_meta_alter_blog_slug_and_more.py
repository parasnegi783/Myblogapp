# Generated by Django 5.1 on 2024-08-30 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_blog_category_alter_blog_meta_alter_blog_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.CharField(default='uncategorized', max_length=255),
        ),
        migrations.AlterField(
            model_name='blog',
            name='meta',
            field=models.CharField(default='No meta information available.', max_length=300),
        ),
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.CharField(default='untitled-blog', max_length=100),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(default='Untitled Blog', max_length=200),
        ),
        migrations.CreateModel(
            name='BlogImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='blog_images/')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='home.blog')),
            ],
        ),
    ]
