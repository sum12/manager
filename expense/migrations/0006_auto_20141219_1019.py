# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_user_many_friends'),
        ('expense', '0005_auto_20141214_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='sharedExpense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expense', models.ForeignKey(to='expense.Expenses')),
                ('sharedWtih', models.ForeignKey(to='user_management.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='expenses',
            name='sharedWith',
        ),
    ]
