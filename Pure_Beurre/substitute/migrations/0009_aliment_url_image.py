# Generated by Django 3.1.2 on 2020-11-16 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0008_delete_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliment',
            name='url_image',
            field=models.URLField(max_length=500, null=True),
        ),
    ]