# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-06 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts_box', '0002_auto_20180305_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='flat_nr',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
