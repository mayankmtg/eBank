# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cust_indiv_account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cust_account_type', models.CharField(default=b'Individual', max_length=250)),
                ('cust_balance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='cust_transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_date', models.DateTimeField(null=True)),
                ('from_account_no', models.IntegerField()),
                ('to_account_no', models.IntegerField()),
                ('Amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='merch_org_account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('merch_account_type', models.CharField(default=b'merch/org', max_length=250)),
                ('merch_balance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_fname', models.CharField(max_length=250)),
                ('user_lname', models.CharField(max_length=250, null=True)),
                ('user_address', models.CharField(max_length=250)),
                ('login_id', models.IntegerField(unique=True)),
                ('password', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='user_type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_super_type', models.CharField(max_length=250)),
                ('user_type', models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='user_info',
            name='user_type_id',
            field=models.ForeignKey(to='vault.user_type'),
        ),
        migrations.AddField(
            model_name='merch_org_account',
            name='merch_user_id',
            field=models.ForeignKey(to='vault.user_info'),
        ),
        migrations.AddField(
            model_name='cust_indiv_account',
            name='cust_user_id',
            field=models.ForeignKey(to='vault.user_info'),
        ),
    ]
