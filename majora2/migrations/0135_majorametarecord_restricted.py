# Generated by Django 2.2.13 on 2020-11-26 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0134_auto_20201110_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='majorametarecord',
            name='restricted',
            field=models.BooleanField(default=False),
        ),
    ]
