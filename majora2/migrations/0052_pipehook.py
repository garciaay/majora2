# Generated by Django 2.2.10 on 2020-04-10 09:30

from django.db import migrations

def bioinfo_process_hook_names(apps, schema_editor):
    DigitalResourceArtifact = apps.get_model("majora2", "DigitalResourceArtifact")
    for dra in DigitalResourceArtifact.objects.filter(current_kind="consensus"):
        if dra.created:
            p = dra.created

            current_name = None
            for record in p.records.all():
                if record.in_artifact:
                    try:
                        if record.in_artifact.dice_name:
                            current_name = record.in_artifact.dice_name
                            break
                    except:
                        pass

            if not p.hook_name and current_name:
                p.hook_name = "bioinfo-%s" % current_name.replace("sequencing-dummy-reads-", "")
                p.save()

class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0051_majoraartifactprocess_hook_name'),
    ]

    operations = [
        migrations.RunPython(bioinfo_process_hook_names),
    ]