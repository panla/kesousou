# Generated by Django 3.0.7 on 2020-08-24 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0007_auto_20200824_0717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='achievement',
            old_name='publish_year',
            new_name='published_year',
        ),
    ]
