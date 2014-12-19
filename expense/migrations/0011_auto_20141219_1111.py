# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0010_remove_sharedexpense_expense'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedexpense',
            name='sharedWtih',
        ),
        migrations.DeleteModel(
            name='sharedExpense',
        ),
    ]
