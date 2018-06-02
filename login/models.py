from django.db import models



class register(models.Model):
    res_username = models.CharField(max_length=30, null=True)
    res_password = models.CharField(max_length=30, null=True)
    res_email = models.CharField(max_length=30, null=True)
    res_id = models.IntegerField( null=True)
    age = models.IntegerField( null=True)
    profession =models.CharField(max_length=30, null=True)
    education =models.IntegerField( null=True)
