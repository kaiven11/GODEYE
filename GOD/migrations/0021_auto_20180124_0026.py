# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-01-23 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GOD', '0020_auto_20180124_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklog',
            name='remote_path',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
