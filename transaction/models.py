from __future__ import unicode_literals

from django.db import models


class TransactionOrder(models.Model):
    counter = models.IntegerField()
    customer = models.IntegerField()
    order = models.IntegerField()
    total = models.IntegerField()
    time = models.DateTimeField(auto_now=True)


class TransactionFunds(models.Model):
    admin = models.IntegerField()
    counter = models.IntegerField()
    total = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
