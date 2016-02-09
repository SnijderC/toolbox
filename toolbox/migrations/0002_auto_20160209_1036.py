# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toolbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advice',
            name='published',
            field=models.BooleanField(default=False, verbose_name=b'Publiseer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='manual',
            name='published',
            field=models.BooleanField(default=False, verbose_name=b'Publiseer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tool',
            name='published',
            field=models.BooleanField(default=False, verbose_name=b'Publiseer'),
            preserve_default=True,
        ),
    ]
