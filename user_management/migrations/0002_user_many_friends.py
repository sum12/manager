# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='many_friends',
            field=models.ManyToManyField(default=None, related_name='many_friends_rel_+', to='user_management.User', blank=True),
            preserve_default=True,
        ),
    ]
