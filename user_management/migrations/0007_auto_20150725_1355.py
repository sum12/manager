# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0019_auto_20150725_1336'),
        ('user_management', '0006_auto_20150725_1352'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
