# Generated by Django 5.1 on 2024-08-30 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_project_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Blog',
        ),
        migrations.RemoveField(
            model_name='project',
            name='technologies',
        ),
        migrations.RemoveField(
            model_name='projectimage',
            name='project',
        ),
        migrations.DeleteModel(
            name='Technology',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='ProjectImage',
        ),
    ]
