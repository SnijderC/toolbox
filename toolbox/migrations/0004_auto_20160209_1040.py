# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toolbox', '0003_auto_20160209_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='is_bad',
            field=models.BooleanField(default=False, help_text=b'Bepaalt of het item in de "Nadelen" lijst te selecteren is.', verbose_name=b'Slechte eigenschap?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='property',
            name='is_good',
            field=models.BooleanField(default=False, help_text=b'Bepaalt of het item in de "Voordelen" lijst te selecteren is.', verbose_name=b'Goede eigenschap?'),
            preserve_default=True,
        ),
    ]
