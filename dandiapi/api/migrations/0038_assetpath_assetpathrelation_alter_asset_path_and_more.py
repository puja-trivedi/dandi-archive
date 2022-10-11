# Generated by Django 4.1.1 on 2022-10-11 19:44

from django.db import migrations, models
import django.db.models.deletion

import dandiapi.api.models.asset


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_alter_version_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetPath',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('path', models.CharField(max_length=512)),
                ('aggregate_files', models.PositiveBigIntegerField(default=0)),
                ('aggregate_size', models.PositiveBigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AssetPathRelation',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('depth', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='asset',
            name='path',
            field=models.CharField(
                max_length=512, validators=[dandiapi.api.models.asset.validate_asset_path]
            ),
        ),
        migrations.AddConstraint(
            model_name='asset',
            constraint=models.CheckConstraint(
                check=models.Q(
                    ('path__regex', '^([A-z0-9(),&\\s#+~_-]?\\/?\\.?[A-z0-9(),&\\s#+~_-])+$')
                ),
                name='asset_path_regex',
            ),
        ),
        migrations.AddConstraint(
            model_name='asset',
            constraint=models.CheckConstraint(
                check=models.Q(('path__startswith', '/'), _negated=True),
                name='asset_path_no_leading_slash',
            ),
        ),
        migrations.AddField(
            model_name='assetpathrelation',
            name='child',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='parent_links',
                to='api.assetpath',
            ),
        ),
        migrations.AddField(
            model_name='assetpathrelation',
            name='parent',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='child_links',
                to='api.assetpath',
            ),
        ),
        migrations.AddField(
            model_name='assetpath',
            name='asset',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='leaf_paths',
                to='api.asset',
            ),
        ),
        migrations.AddField(
            model_name='assetpath',
            name='version',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='asset_paths',
                to='api.version',
            ),
        ),
        migrations.AddConstraint(
            model_name='assetpathrelation',
            constraint=models.UniqueConstraint(
                fields=('parent', 'child'), name='unique-relationship'
            ),
        ),
        migrations.AddConstraint(
            model_name='assetpath',
            constraint=models.CheckConstraint(
                check=models.Q(('path__endswith', '/'), _negated=True), name='consistent-slash'
            ),
        ),
        migrations.AddConstraint(
            model_name='assetpath',
            constraint=models.UniqueConstraint(
                fields=('asset', 'version'), name='unique-asset-version'
            ),
        ),
        migrations.AddConstraint(
            model_name='assetpath',
            constraint=models.UniqueConstraint(
                fields=('version', 'path'), name='unique-version-path'
            ),
        ),
    ]
