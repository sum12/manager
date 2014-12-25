# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0016_sharedexpense'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedexpense',
            name='returned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='expenses',
            name='amount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
