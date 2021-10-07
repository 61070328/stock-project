from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField

# Create your models here.

class Trader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    positions = JSONField(default={'name': "positions"})

    pastReturns = JSONField(default={'name': "pastReturns"})

    cash = models.IntegerField(default=1_000_000)
    AUM = models.IntegerField(default=1_000_000)

    def EMA(data,period=20,column='Close'):
        return data[column].ewm(span=period,adjust=False).mean  