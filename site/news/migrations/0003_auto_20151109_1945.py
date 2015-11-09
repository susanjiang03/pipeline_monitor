# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20151109_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='cat_slug',
        ),
        migrations.RemoveField(
            model_name='article',
            name='news_slug',
        ),
    ]
