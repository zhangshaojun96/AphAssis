# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Recom_guide(models.Model):
	questionId = models.IntegerField(default=0)
	sentence = models.CharField(max_length=60,null=True)
	count = models.IntegerField(default=0)
	value = models.FloatField(default=0.0)
	epsilon = models.FloatField(default=0.3)
	gamma = models.FloatField(default=0.3)
	weight = models.FloatField(default=1.0)
	temperature = models.FloatField(default=0.3)
	alpha = models.FloatField(default=0.5)
	current_arm = models.IntegerField(default=0)
	next_update = models.IntegerField(default=0)
	r = models.IntegerField(default=0)

class Arrange_set(models.Model):
    userid = models.IntegerField(default=0)
    set = models.IntegerField(default=0)
    dateTime = models.DateTimeField(auto_now_add=True)
    # 0 未做  1 完成
    status = models.IntegerField(default=0)

