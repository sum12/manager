# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0009_remove_sharedexpense_t'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedexpense',
            name='expense',
        ),
    ]
