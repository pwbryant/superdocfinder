# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0011_auto_20160309_1818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='abstract',
            new_name='title',
        ),
    ]
