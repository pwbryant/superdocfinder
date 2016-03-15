# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0013_auto_20160314_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='doc_id',
            field=models.IntegerField(unique=True),
        ),
    ]
