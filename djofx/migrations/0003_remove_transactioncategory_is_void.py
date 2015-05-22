# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djofx', '0002_add_category_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactioncategory',
            name='is_void',
        ),
    ]
