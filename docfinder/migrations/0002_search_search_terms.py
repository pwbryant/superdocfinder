# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='search_terms',
            field=models.TextField(default=''),
        ),
    ]
