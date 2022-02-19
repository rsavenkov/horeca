# Generated by Django 3.1.4 on 2021-02-15 22:25

from django.db import migrations, models
import django.db.models.deletion

from candidate_tests.utils import testing_data_parser

def create_MMPI_risk_factors(apps, schema_editor, sheet_name):
    MMPIScale = apps.get_model('candidate_tests', 'MMPIScale')
    MMPIRiskFactor = apps.get_model('candidate_tests', 'MMPIRiskFactor')
    factors = testing_data_parser.parse_MMPI_risk_factors(sheet_name)

    for i in factors:
        scales = MMPIScale.objects.filter(name=i['scale'])
        i.pop('scale')
        for s in scales:
            MMPIRiskFactor.objects.update_or_create(
                scale=s,
                **i,
            )

def MMPI_risk_factors(apps, schema_editor):
    create_MMPI_risk_factors(apps, schema_editor, sheet_name='Risk factors')

def MMPI_attantion_factors(apps, schema_editor):
    create_MMPI_risk_factors(apps, schema_editor, sheet_name='Attantion factors')


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0023_mmpidestructors_mmpimotivators'),
    ]

    operations = [
        migrations.CreateModel(
            name='MMPIRiskFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_point', models.PositiveIntegerField()),
                ('to_point', models.PositiveIntegerField()),
                ('factor', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_attantion_factor', models.BooleanField(default=False)),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risk_factors', to='candidate_tests.mmpiscale')),
            ],
            options={
                'verbose_name': 'ММИЛ фактор риска',
                'verbose_name_plural': 'ММИЛ факторы риска',
            },
        ),
        migrations.RunPython(MMPI_risk_factors),
        migrations.RunPython(MMPI_attantion_factors),
    ]