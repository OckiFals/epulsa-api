from __future__ import unicode_literals

from django.db import models
from users.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    purchase = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "#%s:%s" % (self.id, self.customer)

    class Meta:
        ordering = ('time',)
