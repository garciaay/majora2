# Generated by Django 2.2.10 on 2020-04-05 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0045_remove_biosampleartifact_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='dnasequencingprocess',
            name='run_group',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='abstractbioinformaticsprocess',
            name='pipe_name',
            field=models.CharField(blank=True, max_length=96, null=True),
        ),
    ]
