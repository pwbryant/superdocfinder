# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0002_search_search_terms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('doc_id', models.TextField(default='', unique=True)),
                ('filename', models.TextField(default='', unique=True)),
                ('author', models.TextField(default='')),
                ('abstract', models.TextField(default='')),
            ],
        ),
    ]
