# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0008_auto_20160115_0444'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='tags',
            field=tagging.fields.TagField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 1, 18, 15, 46, 11, 295426), null=True, verbose_name='Message date'),
        ),
    ]
