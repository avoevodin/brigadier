# Generated by Django 3.1.7 on 2021-03-24 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20210324_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, choices=[(None, ''), ('new', 'New'), ('completed', 'Completed'), ('processed', 'Processed')], default=None, max_length=20, null=True, verbose_name='status'),
        ),
    ]
