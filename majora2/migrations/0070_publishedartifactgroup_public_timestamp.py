# Generated by Django 2.2.10 on 2020-05-04 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0069_pagqualityreportequivalencegroup_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishedartifactgroup',
            name='public_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]