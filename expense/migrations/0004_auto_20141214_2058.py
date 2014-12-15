# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0003_auto_20141213_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='tag',
            field=models.CharField(default=None, max_length=100),
            preserve_default=True,
        ),
    ]
