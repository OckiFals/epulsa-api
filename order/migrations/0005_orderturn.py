# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-31 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20160530_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTurn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.IntegerField()),
                ('count', models.IntegerField()),
            ],
        ),
    ]
