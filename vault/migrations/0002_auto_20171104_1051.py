# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-04 10:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vault', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registerrequests',
            name='user',
        ),
        migrations.AddField(
            model_name='registerrequests',
            name='user_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
