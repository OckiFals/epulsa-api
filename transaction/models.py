from __future__ import unicode_literals

from django.db import models

CHOICES_TYPE = (
    (1, 'Order Pulsa'),
    (2, 'Cairkan Dana')
)


class TransactionCustomer(models.Model):
    customer = models.IntegerField()
    user2 = models.IntegerField()
    type = models.IntegerField(choices=CHOICES_TYPE)
    total = models.IntegerField()
    time = models.DateTimeField(auto_now=True)


class TransactionCounter(models.Model):
    counter = models.IntegerField()
    user2 = models.IntegerField()
    type = models.IntegerField(choices=CHOICES_TYPE)
    total = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
