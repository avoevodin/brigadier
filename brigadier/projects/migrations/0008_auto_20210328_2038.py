# Generated by Django 3.1.7 on 2021-03-28 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20210325_2344'),
        ('projects', '0007_auto_20210326_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks_assignee', to='employees.employee', verbose_name='Assignee'),
        ),
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks_author', to='employees.employee', verbose_name='Author'),
        ),
    ]
