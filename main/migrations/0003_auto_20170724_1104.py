# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-24 11:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_contactmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmessage',
            old_name='Message',
            new_name='message',
        ),
    ]