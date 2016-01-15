# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='account_rep',
            field=models.ForeignKey(default=0, to='db.UserProfile', related_name='rep'),
        ),
    ]
