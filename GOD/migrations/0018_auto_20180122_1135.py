# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-01-22 11:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GOD', '0017_tasklog_host_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetail',
            name='children_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GOD.TaskLog'),
        ),
    ]
