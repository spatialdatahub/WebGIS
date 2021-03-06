# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-05 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('keyword_slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('datasets', models.ManyToManyField(to='datasets.Dataset')),
            ],
        ),
    ]
