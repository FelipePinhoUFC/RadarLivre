# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-28 05:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radarlivre_api', '0006_auto_20160328_0039'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Route',
            new_name='Flight',
        ),
        migrations.RenameField(
            model_name='airplaneinfo',
            old_name='route',
            new_name='flight',
        ),
        migrations.RenameField(
            model_name='observation',
            old_name='route',
            new_name='flight',
        ),
    ]
