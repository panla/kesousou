# Generated by Django 3.0.7 on 2020-08-24 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0006_auto_20200824_0712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodical',
            name='first_creator',
            field=models.CharField(max_length=30, null=True, verbose_name='第一作者'),
        ),
    ]
