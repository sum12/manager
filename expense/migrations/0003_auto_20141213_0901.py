# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_auto_20141213_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='sharedWith',
            field=models.ForeignKey(related_name='+', default=None, to='user_management.User', null=True),
            preserve_default=True,
        ),
    ]
