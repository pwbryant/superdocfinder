# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0009_auto_20160205_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('doc_id', models.ForeignKey(to='docfinder.Document')),
                ('searches_id', models.ForeignKey(to='docfinder.Searches')),
            ],
        ),
    ]
