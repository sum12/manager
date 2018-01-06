# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0008_auto_20150725_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='friends',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT),
            preserve_default=True,
        ),
    ]
