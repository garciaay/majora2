# Generated by Django 2.2.13 on 2020-08-07 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tatl', '0008_tatltask'),
    ]

    operations = [
        migrations.AddField(
            model_name='tatltask',
            name='payload',
            field=models.TextField(default='{}'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tatltask',
            name='state',
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
        migrations.AddField(
            model_name='tatltask',
            name='substitute_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='su_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
