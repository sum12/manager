# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_user_many_friends'),
        ('expense', '0011_auto_20141219_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='sharedExpense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('sharedWtih', models.ForeignKey(to='user_management.User',
                                                 on_delete=models.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
