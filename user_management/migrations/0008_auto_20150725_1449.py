# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0007_auto_20150725_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='date_of_birth',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
