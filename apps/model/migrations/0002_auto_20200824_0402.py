# Generated by Django 3.0.7 on 2020-08-24 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='location',
        ),
        migrations.RemoveField(
            model_name='user',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='user',
            name='updated_at',
        ),
    ]