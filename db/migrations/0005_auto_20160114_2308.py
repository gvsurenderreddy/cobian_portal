# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_auto_20160114_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_date',
            field=models.DateTimeField(blank=True, verbose_name='Message date', null=True, default=datetime.datetime(2016, 1, 14, 23, 8, 51, 119934)),
        ),
    ]
