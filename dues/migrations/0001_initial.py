# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-06-15 02:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0015_auto_20180413_0711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_charge', models.FloatField(default=0.0)),
                ('net', models.FloatField(default=0.0)),
                ('print_scan', models.FloatField(default=0.0)),
                ('canteen', models.FloatField(default=0.0)),
                ('recreation', models.FloatField(default=0.0)),
                ('mess', models.FloatField(default=0.0)),
                ('mess_bill', models.FloatField(blank=True, default=0.0)),
                ('library', models.FloatField(default=0.0)),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.Boarder')),
            ],
        ),
    ]
