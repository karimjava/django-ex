# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='ask_id',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='image_path',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
