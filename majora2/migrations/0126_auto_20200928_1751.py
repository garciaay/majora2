# Generated by Django 2.2.13 on 2020-09-28 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0125_auto_20200908_1617'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='biosampleartifact',
            options={'permissions': [('force_add_biosampleartifact', 'Can forcibly add a biosample artifact to Majora')]},
        ),
    ]
