# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-26 12:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_photo_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='path',
            new_name='visible_name',
        ),
    ]
