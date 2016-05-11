from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

PROVIDER = (
    (1, 'OOREDO'),
    (2, 'XL'),
    (3, 'TELKOMSEL'),
    (4, 'Three')
)

IS_ONLINE = (
    (1, 'Online'),
    (2, 'Offline')
)


class Customer(models.Model):
    user = models.OneToOneField(User, unique=True)
    phone = models.CharField(max_length=15)
    provider = models.IntegerField(choices=PROVIDER)
    saldo = models.IntegerField(default=0)
    type = models.IntegerField(default=3)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ('user',)


class Counter(models.Model):
    user = models.OneToOneField(User, unique=True)
    store_name = models.CharField(max_length=18)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    saldo = models.IntegerField(default=0)
    income = models.IntegerField(default=0)
    is_online = models.IntegerField(choices=IS_ONLINE)

    def __unicode__(self):
        return self.store_name

    class Meta:
        ordering = ('user', 'is_online')
