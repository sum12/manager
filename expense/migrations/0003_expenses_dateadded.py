# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_expenses_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='dateAdded',
            field=models.DateField(default=datetime.datetime(1, 1, 1, 0, 0), auto_now_add=True),
            preserve_default=True,
        ),
    ]
