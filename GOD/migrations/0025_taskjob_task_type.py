# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-01-30 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GOD', '0024_auto_20180130_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskjob',
            name='task_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'sshtask'), (1, 'scptask'), (2, 'gittask')], default=0),
        ),
    ]
