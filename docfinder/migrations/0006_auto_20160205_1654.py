# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0005_searches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searches',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
