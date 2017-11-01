# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0003_auto_20171024_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='registerRequests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('e_mail', models.CharField(max_length=250)),
            ],
        ),
    ]
