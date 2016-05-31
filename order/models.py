from __future__ import unicode_literals

from django.db import models
from users.models import Customer, Counter

STATUS = (
    (1, 'New'),
    (2, 'Waiting'),
    (3, 'Done')
)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    purchase = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    status = models.IntegerField(choices=STATUS, default=1)
    time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "#%s:%s" % (self.id, self.customer)

    class Meta:
        ordering = ('time',)


class OrderTurn(models.Model):
    turn = models.IntegerField()
    count = models.IntegerField()
