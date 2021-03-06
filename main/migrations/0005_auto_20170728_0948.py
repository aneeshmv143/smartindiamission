# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-28 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_useractivation'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='mobile_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='nature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='reg_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='reg_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
