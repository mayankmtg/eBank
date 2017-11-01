# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0004_registerrequests'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerrequests',
            name='group',
            field=models.CharField(default=datetime.datetime(2017, 11, 1, 9, 12, 6, 630055, tzinfo=utc), max_length=250),
            preserve_default=False,
        ),
    ]
