# Generated by Django 3.1.7 on 2021-03-25 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_auto_20210325_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='firstname',
            field=models.CharField(max_length=200, verbose_name='Firstname'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='surname',
            field=models.CharField(max_length=200, verbose_name='Surname'),
        ),
    ]
