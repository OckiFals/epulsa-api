from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

PROVIDER = (
    (1, 'OOREDO'),
    (2, 'XL'),
    (3, 'TELKOMSEL'),
    (4, 'Three')
)


class Customer(models.Model):
    user = models.OneToOneField(User, unique=False)
    phone = models.CharField(max_length=15)
    provider = models.IntegerField(choices=PROVIDER)
    saldo = models.IntegerField(default=0)
    type = models.IntegerField(default=3)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ('user',)
