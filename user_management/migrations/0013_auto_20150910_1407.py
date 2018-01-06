# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0012_delete_person'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together=set([('f1', 'f2')]),
        ),
    ]
