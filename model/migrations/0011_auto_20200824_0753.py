# Generated by Django 3.0.7 on 2020-08-24 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0010_auto_20200824_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='sn',
            field=models.CharField(db_index=True, max_length=100, null=True, verbose_name='项目年度编号'),
        ),
        migrations.AlterField(
            model_name='periodical',
            name='doi',
            field=models.CharField(db_index=True, max_length=100, null=True, verbose_name='doi'),
        ),
    ]