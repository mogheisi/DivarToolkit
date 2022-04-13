from django.db import models


class DailyPrice(models.Model):
    name = models.CharField(max_length=128)
    price = models.CharField(max_length=32)
    detail = models.CharField(max_length=128)
    changes = models.CharField(max_length=128)
