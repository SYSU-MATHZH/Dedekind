# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-14 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sua', '0011_auto_20170713_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='sua_application',
            name='feedback',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='sua',
            name='team',
            field=models.CharField(default='无分组', max_length=200),
        ),
    ]
