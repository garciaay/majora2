# Generated by Django 2.2.10 on 2020-04-27 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0065_auto_20200426_0232'),
    ]

    operations = [
        migrations.CreateModel(
            name='PAGQualityTestEquivalenceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=64, null=True)),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='pagqualityreport',
            name='is_skip',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pagqualityreportgroup',
            name='is_skip',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pagqualitytest',
            name='slug',
            field=models.SlugField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='pagqualityreportgroup',
            name='pag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='quality_tests', to='majora2.PublishedArtifactGroup'),
        ),
        migrations.CreateModel(
            name='PAGQualityTestFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_name', models.CharField(max_length=64)),
                ('filter_desc', models.CharField(max_length=128)),
                ('force_field', models.BooleanField(default=True)),
                ('metadata_namespace', models.CharField(blank=True, max_length=64, null=True)),
                ('metadata_name', models.CharField(blank=True, max_length=64, null=True)),
                ('filter_on_str', models.CharField(max_length=64)),
                ('op', models.CharField(blank=True, max_length=3, null=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='filters', to='majora2.PAGQualityTest')),
            ],
        ),
        migrations.CreateModel(
            name='PAGQualityReportEquivalenceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_pass', models.BooleanField(default=False)),
                ('pag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='quality_groups', to='majora2.PublishedArtifactGroup')),
                ('test_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='report_groups', to='majora2.PAGQualityTestEquivalenceGroup')),
            ],
        ),
        migrations.AddField(
            model_name='pagqualityreportgroup',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='quality_tests', to='majora2.PAGQualityReportEquivalenceGroup'),
        ),
        migrations.AddField(
            model_name='pagqualitytest',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tests', to='majora2.PAGQualityTestEquivalenceGroup'),
        ),
    ]