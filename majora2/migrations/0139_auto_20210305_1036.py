# Generated by Django 2.2.13 on 2021-03-05 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0138_librarypoolingprocessrecord_sequencing_org_received_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishedartifactgroup',
            name='published_name',
            field=models.CharField(db_index=True, max_length=128),
        ),
    ]
