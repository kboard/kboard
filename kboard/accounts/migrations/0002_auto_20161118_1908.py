# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-18 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='fullname',
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
