# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-01-18 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GOD', '0014_remove_tasklog_hosts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetail',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'failed'), (1, 'sucess'), (2, 'unknow')]),
        ),
    ]
