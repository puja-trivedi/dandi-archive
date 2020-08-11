# Generated by Django 3.0.9 on 2020-08-10 15:22

from django.db import migrations


def populate_drafts(apps, schema_editor):
    Dandiset = apps.get_model('publish', 'Dandiset')  # noqa: N806
    Version = apps.get_model('publish', 'Version')  # noqa: N806
    DraftVersion = apps.get_model('publish', 'DraftVersion')  # noqa: N806

    for dandiset in Dandiset.objects.all():
        if DraftVersion.objects.filter(dandiset=dandiset).exists():
            continue
        latest_version = Version.objects.filter(dandiset=dandiset).order_by('-version')[0]
        draft = DraftVersion(
            dandiset=dandiset,
            name=latest_version.name,
            description=latest_version.description,
            metadata=latest_version.metadata,
        )
        draft.save()


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0005_add_drafts_model'),
    ]

    operations = [
        migrations.RunPython(populate_drafts, reverse_code=migrations.RunPython.noop),
    ]
