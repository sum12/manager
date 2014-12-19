# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0013_auto_20141219_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sharedexpense',
            old_name='wiih',
            new_name='wit',
        ),
    ]
