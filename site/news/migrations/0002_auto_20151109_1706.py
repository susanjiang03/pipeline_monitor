# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newspaper', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=15)),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('description', models.CharField(max_length=200)),
                ('news_slug', models.SlugField(unique=True)),
                ('cat_slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='RSS',
        ),
    ]
