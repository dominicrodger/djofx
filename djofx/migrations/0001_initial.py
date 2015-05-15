# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_key', models.CharField(max_length=255)),
                ('amount', models.DecimalField(max_digits=15, decimal_places=2)),
                ('date', models.DateField()),
                ('payee', models.CharField(max_length=255)),
                ('transaction_type', models.CharField(max_length=255)),
                ('category_verified', models.BooleanField(default=False)),
                ('account', models.ForeignKey(to='djofx.Account')),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('is_void', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_category',
            field=models.ForeignKey(blank=True, to='djofx.TransactionCategory', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('account', 'transaction_key')]),
        ),
    ]
