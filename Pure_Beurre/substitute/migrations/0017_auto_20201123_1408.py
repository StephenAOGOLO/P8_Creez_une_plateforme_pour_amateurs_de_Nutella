# Generated by Django 3.1.2 on 2020-11-23 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0016_remove_customer_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='user_id',
            new_name='user',
        ),
    ]
