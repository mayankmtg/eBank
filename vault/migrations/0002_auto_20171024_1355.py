# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cust_transaction',
            name='transaction_date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
