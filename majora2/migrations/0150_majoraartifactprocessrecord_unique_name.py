# Generated by Django 2.2.27 on 2022-02-26 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0149_institute_credit_code_only'),
    ]

    operations = [
        migrations.AddField(
            model_name='majoraartifactprocessrecord',
            name='unique_name',
            field=models.CharField(max_length=128, null=True, unique=True),
        ),
    ]