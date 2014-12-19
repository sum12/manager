# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0007_sharedexpense_t'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedexpense',
            name='sharedWtih',
            field=models.ForeignKey(to='user_management.User', null=True),
            preserve_default=True,
        ),
    ]
