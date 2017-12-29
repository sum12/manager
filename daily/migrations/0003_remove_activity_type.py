# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daily', '0002_auto_20171229_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='type',
        ),
    ]
