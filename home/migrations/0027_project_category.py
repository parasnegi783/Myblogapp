# Generated by Django 5.1 on 2024-09-09 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_blog_certificate_project_p_favorited'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.CharField(blank=True, default='uncategorized', max_length=255, null=True),
        ),
    ]
