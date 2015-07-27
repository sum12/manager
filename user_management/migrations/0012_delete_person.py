# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0011_remove_person_friends'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
    ]
