# Generated by Django 5.1 on 2024-08-30 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='sno',
            new_name='id',
        ),
    ]
