# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='cust_transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_date', models.DateTimeField(null=True)),
                ('pending', models.BooleanField(default=True)),
                ('Amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='user_account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cust_account_type', models.CharField(default=b'Individual', max_length=250)),
                ('cust_balance', models.FloatField()),
                ('cust_user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
            model_name='cust_transaction',
            name='from_account',
            field=models.ForeignKey(related_name='from_account', to='vault.user_account'),
        ),
        migrations.AddField(
            model_name='cust_transaction',
            name='to_account',
            field=models.ForeignKey(related_name='to_account', to='vault.user_account'),
        ),
    ]
