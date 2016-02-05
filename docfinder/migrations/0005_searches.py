# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0004_auto_20160205_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='Searches',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('time', models.DateTimeField()),
                ('search_id', models.ForeignKey(to='docfinder.Search')),
            ],
        ),
    ]
