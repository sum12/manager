# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0003_expenses_dateadded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='sharedWith',
            field=models.ForeignKey(related_name='+', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='expenses',
            name='spender',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
