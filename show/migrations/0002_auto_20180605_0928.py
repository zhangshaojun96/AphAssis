# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-05 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arrange_set',
            old_name='dateTime',
            new_name='arrTime',
        ),
        migrations.AddField(
            model_name='arrange_set',
            name='finTime',
            field=models.DateTimeField(null=True),
        ),
    ]
