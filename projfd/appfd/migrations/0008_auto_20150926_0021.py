# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appfd', '0007_auto_20150922_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alias',
            name='language',
            field=models.CharField(max_length=7),
        ),
    ]
