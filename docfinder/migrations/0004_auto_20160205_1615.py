# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0003_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='search_terms',
            field=models.TextField(unique=True, default=''),
        ),
    ]
