# Generated by Django 2.2.13 on 2021-01-14 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0137_auto_20210113_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarypoolingprocessrecord',
            name='sequencing_org_received_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
