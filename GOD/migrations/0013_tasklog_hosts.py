# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-01-18 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GOD', '0012_auto_20180118_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklog',
            name='hosts',
            field=models.ManyToManyField(to='GOD.BindHosts'),
        ),
    ]
