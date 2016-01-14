# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import db.models.user_profile


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_auto_20160114_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='account_id',
            field=models.CharField(null=True, blank=True, max_length=50, verbose_name='Account Id'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='account_rep',
            field=models.ForeignKey(default=0, blank=True, null=True, related_name='rep', to='db.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='company',
            field=models.CharField(null=True, blank=True, max_length=100, verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='notes',
            field=models.TextField(default='', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(null=True, blank=True, max_length=30, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='shipping_method',
            field=models.CharField(null=True, blank=True, max_length=50, verbose_name='Shipping Method'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='terms',
            field=models.CharField(null=True, blank=True, max_length=50, verbose_name='Terms'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='terms_file_path',
            field=models.FileField(null=True, upload_to=db.models.user_profile.get_terms_upload_to),
        ),
    ]
