# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-02 10:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0003_auto_20180602_0827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arrange_set',
            name='usedTime',
        ),
        migrations.RemoveField(
            model_name='arrange_set',
            name='wrong_ques',
        ),
    ]
