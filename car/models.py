import datetime

from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=128)
    color = models.CharField(max_length=32)
    kilometer = models.CharField(max_length=32)
    model = models.CharField(max_length=4)
    price = models.CharField(max_length=32)
    link = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class DailyPrice(models.Model):
    name = models.CharField(max_length=128)
    price = models.CharField(max_length=32)
    detail = models.CharField(max_length=128)
    changes = models.CharField(max_length=128)
