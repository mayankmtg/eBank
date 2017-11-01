# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0002_auto_20171101_1219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registerrequests',
            old_name='user',
            new_name='user_data',
        ),
    ]
