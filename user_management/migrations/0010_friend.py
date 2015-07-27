# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0009_auto_20150725_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('since', models.DateField(default=django.utils.timezone.now)),
                ('f1', models.ForeignKey(related_name='friends_with', to=settings.AUTH_USER_MODEL)),
                ('f2', models.ForeignKey(related_name='friends_of', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
