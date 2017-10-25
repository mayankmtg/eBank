# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0002_auto_20171024_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cust_transaction',
            name='transaction_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
