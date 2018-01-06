# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


def copy_typestotypeoder(apps, schema_editor):
    activity = apps.get_model('daily.activity')
    typeorder = apps.get_model('daily.typeorder')
    tos = []
    alltypes = set(act.type for act in activity.objects.all())
    for odr, type in enumerate(alltypes):
        to = typeorder()
        to.type = type
        to.order = odr
        to.save()
        tos += [(type, to)]

    for act in activity.objects.all():
        act.type_order = [to[1] for to in tos if to[0] == act.type][0]
        act.type = ''
        act.save()


class Migration(migrations.Migration):

    dependencies = [
        ('daily', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='typeorder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ('-on',)},
        ),
        migrations.AddField(
            model_name='activity',
            name='type_order',
            field=models.ForeignKey(default=0, to='daily.typeorder',
                                    on_delete=models.PROTECT),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activity',
            name='on',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.RunPython(copy_typestotypeoder)
    ]
