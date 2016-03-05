# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toolbox', '0002_auto_20160209_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='published',
            field=models.BooleanField(default=False, verbose_name=b'Publiseer'),
            preserve_default=True,
        ),
    ]
