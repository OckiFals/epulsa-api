# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-07 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20160506_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='type',
            field=models.IntegerField(default=3),
        ),
    ]
