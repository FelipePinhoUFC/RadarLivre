# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-28 06:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radarlivre_api', '0007_auto_20160328_0232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='halfobservation',
            old_name='route',
            new_name='flight',
        ),
    ]
