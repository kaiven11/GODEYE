# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-04 15:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GOD', '0031_auto_20180201_2239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskplan',
            old_name='name',
            new_name='planame',
        ),
        migrations.RenameField(
            model_name='taskstage',
            old_name='name',
            new_name='stagename',
        ),
    ]
