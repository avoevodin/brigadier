# Generated by Django 3.1.7 on 2021-03-24 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_auto_20210324_1917'),
        ('projects', '0003_auto_20210324_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='executor',
        ),
        migrations.AddField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_assignee', to='employees.employee', verbose_name='Assignee'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('completed', 'Completed'), ('processed', 'Processed')], default='new', max_length=20, verbose_name='status'),
        ),
    ]
