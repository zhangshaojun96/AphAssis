from __future__ import unicode_literals
from django.db import models



# Create your models here.

class QuestionSet(models.Model):
	setId = models.IntegerField()
	setDes = models.CharField(max_length=200, null=True)
	questions = models.CharField(max_length=200,null=True)

	def __unicode__(self):
		return self.questions
