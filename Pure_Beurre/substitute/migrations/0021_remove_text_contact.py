# Generated by Django 3.1.2 on 2020-12-21 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0020_auto_20201221_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='contact',
        ),
    ]
