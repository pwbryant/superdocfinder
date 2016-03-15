# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0012_auto_20160314_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='author',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='document',
            name='doc_id',
            field=models.CharField(unique=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='document',
            name='filename',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.TextField(unique=True),
        ),
    ]
