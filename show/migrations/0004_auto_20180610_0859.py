# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-10 08:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0003_wrong_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wrong_record',
            name='guide',
            field=models.IntegerField(default=0),
        ),
    ]