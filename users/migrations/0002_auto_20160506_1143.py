# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-06 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='saldo',
            field=models.IntegerField(),
        ),
    ]