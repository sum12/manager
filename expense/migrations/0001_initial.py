# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateAdded', models.DateField(default=datetime.datetime(1, 1, 1, 0, 0), auto_now_add=True)),
                ('amount', models.IntegerField(default=0)),
                ('tag', models.CharField(default=None, max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
