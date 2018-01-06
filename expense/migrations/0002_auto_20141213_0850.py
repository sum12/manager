# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='sharedWith',
            field=models.ForeignKey(related_name='+', default=None,
                                    to='user_management.User',
                                    on_delete=models.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expenses',
            name='spender',
            field=models.ForeignKey(to='user_management.User',
                                    on_delete=models.PROTECT),
            preserve_default=True,
        ),
    ]
