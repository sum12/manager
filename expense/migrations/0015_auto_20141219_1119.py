# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0014_auto_20141219_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedexpense',
            name='wit',
        ),
        migrations.DeleteModel(
            name='sharedExpense',
        ),
    ]
