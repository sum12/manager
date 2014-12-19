# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0006_auto_20141219_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedexpense',
            name='t',
            field=models.CharField(default=b'', max_length=b'100'),
            preserve_default=True,
        ),
    ]
