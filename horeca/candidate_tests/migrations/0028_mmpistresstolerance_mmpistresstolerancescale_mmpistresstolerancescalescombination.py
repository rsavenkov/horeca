# Generated by Django 3.1.4 on 2021-02-23 17:21

from django.db import migrations, models
import django.db.models.deletion

from candidate_tests.utils import testing_data_parser
from horeca_utils import constants


def MMPI_stress_tolerances(apps, schema_editor):
    MMPIStressTolerance = apps.get_model('candidate_tests', 'MMPIStressTolerance')
    values = testing_data_parser.parse_MMPI_stress_tolerance()

    for v in values:
        MMPIStressTolerance.objects.update_or_create(**v)


def MMPI_stress_tolerance_scales(apps, schema_editor):
    MMPIStressTolerance = apps.get_model('candidate_tests', 'MMPIStressTolerance')
    MMPIStressToleranceScale = apps.get_model('candidate_tests', 'MMPIStressToleranceScale')
    MMPIStressToleranceScalesCombination = apps.get_model('candidate_tests', 'MMPIStressToleranceScalesCombination')
    MMPIScale = apps.get_model('candidate_tests', 'MMPIScale')

    scales_combinations = testing_data_parser.parse_MMPI_stress_tolerance_scales()

    for stress_tolerance in constants.MMPIStressTolerances:
        for scales_combination in scales_combinations[stress_tolerance.value]:
            combination = MMPIStressToleranceScalesCombination.objects.create(
                stress_tolerance=MMPIStressTolerance.objects.get(name=stress_tolerance.value)
            )
            for s in scales_combination:
                scale = MMPIScale.objects.get(name=s['scale'])
                s.pop('scale')
                MMPIStressToleranceScale.objects.create(
                    scale=scale,
                    combination=combination,
                    **s,
                )


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0027_mmpiteamrole_mmpiteamrolescale'),
    ]

    operations = [
        migrations.CreateModel(
            name='MMPIStressTolerance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Высокий', 'Высокий'), ('Средний', 'Средний'), ('Низкий', 'Низкий')], max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'ММИЛ тип стрессоустойчивости',
                'verbose_name_plural': 'ММИЛ типы стрессоустойчивости',
            },
        ),
        migrations.CreateModel(
            name='MMPIStressToleranceScalesCombination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stress_tolerance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scales_combinations', to='candidate_tests.mmpistresstolerance')),
            ],
            options={
                'verbose_name': 'ММИЛ стрессоустойчивость комбинация шкал',
                'verbose_name_plural': 'ММИЛ стрессоустойчивость комбинации шкал',
            },
        ),
        migrations.CreateModel(
            name='MMPIStressToleranceScale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_point', models.PositiveIntegerField()),
                ('to_point', models.PositiveIntegerField()),
                ('combination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scales', to='candidate_tests.mmpistresstolerancescalescombination')),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stress_tolerance_scales', to='candidate_tests.mmpiscale')),
            ],
            options={
                'verbose_name': 'ММИЛ шкала стрессоустойчивости',
                'verbose_name_plural': 'ММИЛ шкалы стрессоустойчивости',
            },
        ),
        migrations.RunPython(MMPI_stress_tolerances),
        migrations.RunPython(MMPI_stress_tolerance_scales),
    ]