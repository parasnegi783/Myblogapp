# Generated by Django 5.1 on 2024-09-09 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='meta',
            field=models.CharField(blank=True, default='No meta information available.', max_length=300, null=True),
        ),
    ]