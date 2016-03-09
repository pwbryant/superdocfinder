# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0010_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='search_terms',
            field=models.TextField(unique=True),
        ),
    ]
