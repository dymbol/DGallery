# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-26 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0005_auto_20170914_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='type',
            field=models.CharField(default='jpg', max_length=10),
            preserve_default=False,
        ),
    ]
