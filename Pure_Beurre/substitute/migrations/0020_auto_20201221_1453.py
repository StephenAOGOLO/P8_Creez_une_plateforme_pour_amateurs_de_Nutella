# Generated by Django 3.1.2 on 2020-12-21 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0019_auto_20201221_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='footer',
        ),
        migrations.RemoveField(
            model_name='text',
            name='home',
        ),
        migrations.AddField(
            model_name='text',
            name='contact',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='home_bm',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='home_c',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='home_s',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_a_cgv',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_a_fn',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_a_rcs',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_cookies',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_id_fn',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_id_ln',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_id_m',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_id_ph',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_id_pn',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_id_s',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='mentions_title',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
