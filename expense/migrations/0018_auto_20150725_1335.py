# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0017_auto_20141225_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedexpense',
            name='wit',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
