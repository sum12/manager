# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0012_sharedexpense'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sharedexpense',
            old_name='sharedWtih',
            new_name='wiih',
        ),
    ]
