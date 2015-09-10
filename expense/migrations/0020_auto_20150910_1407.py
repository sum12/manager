# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0019_auto_20150725_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='pinned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='expenses',
            name='dateAdded',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
