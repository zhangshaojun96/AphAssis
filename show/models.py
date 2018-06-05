# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Recom_guide(models.Model):
    questionId = models.IntegerField(default=0)
    sentence = models.CharField(max_length=60, null=True)
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
    arrTime = models.DateTimeField(auto_now_add=True)
    finTime = models.DateTimeField(null=True)
    # 0 未做  1 完成
    status = models.IntegerField(default=0)
    # 如果做了的话,记录时间
    usedTime = models.FloatField(default=0.0)
    # 格式：按照答题顺序排序，'q#rg,q#rg,q#rg'，其中q指的是问题id，rq指的是使得患者答对问题的引导语id
    wrong_ques = models.CharField(max_length=300, null=True)
