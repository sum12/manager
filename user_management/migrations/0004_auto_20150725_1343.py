# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0019_auto_20150725_1336'),
        ('user_management', '0003_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='friends',
        ),
    ]
