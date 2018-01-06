# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr',
                    models.OneToOneField(parent_link=True, auto_created=True,
                                         to=settings.AUTH_USER_MODEL,
                                         on_delete=models.PROTECT,
                                         primary_key=True, serialize=False)),
                ('friends', models.ForeignKey(default=None, null=True,
                                              to='user_management.User',
                                              on_delete=models.PROTECT)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
    ]
