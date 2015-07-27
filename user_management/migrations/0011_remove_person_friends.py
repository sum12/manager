# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0010_friend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='friends',
        ),
    ]
