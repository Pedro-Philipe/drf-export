from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    age = models.IntegerField()