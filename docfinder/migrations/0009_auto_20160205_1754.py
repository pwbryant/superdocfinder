# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0008_auto_20160205_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searches',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
