# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-01-18 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GOD', '0011_auto_20180118_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetail',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'failed'), ('1', 'sucess')]),
        ),
    ]
