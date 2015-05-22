# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djofx', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transactioncategory',
            options={'ordering': ('name',), 'verbose_name_plural': 'Transaction categories'},
        ),
        migrations.AddField(
            model_name='transactioncategory',
            name='category_type',
            field=models.CharField(default=b'out', max_length=3, choices=[(b'out', b'Outgoings'), (b'inc', b'Income'), (b'int', b'Internal Transfer')]),
        ),
        migrations.AlterField(
            model_name='transactioncategory',
            name='is_void',
            field=models.BooleanField(default=False, help_text=b'Transactions in internal transfer categories will be hidden from charts - this is useful for transfers between your accounts.', verbose_name=b'Tracks Internal Transfers'),
        ),
    ]
