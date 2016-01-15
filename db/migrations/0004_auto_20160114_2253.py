# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import db.models.user_profile


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_auto_20160114_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='account_rep',
            field=models.ForeignKey(to='db.UserProfile', related_name='rep', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='terms_file_path',
            field=models.FileField(blank=True, upload_to=db.models.user_profile.get_terms_upload_to, null=True),
        ),
    ]
