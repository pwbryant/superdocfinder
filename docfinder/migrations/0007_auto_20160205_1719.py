# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docfinder', '0006_auto_20160205_1654'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Documents',
            new_name='Document',
        ),
    ]
