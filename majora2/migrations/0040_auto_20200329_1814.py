# Generated by Django 2.2.10 on 2020-03-29 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0039_biosourcesamplingprocess_received_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='biosampleartifact',
            old_name='sample_type_curent',
            new_name='sample_type_current',
        ),
    ]
