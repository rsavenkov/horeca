# Generated by Django 3.1.4 on 2021-02-17 12:35

from django.db import migrations, models
import django.db.models.deletion

from candidate_tests.utils import testing_data_parser


def MMPI_team_roles(apps, schema_editor):
    MMPITeamRole = apps.get_model('candidate_tests', 'MMPITeamRole')
    values = testing_data_parser.parse_MMPI_team_roles()

    for v in values:
        MMPITeamRole.objects.update_or_create(**v)

def MMPI_team_role_scales(apps, schema_editor):
    MMPITeamRole = apps.get_model('candidate_tests', 'MMPITeamRole')
    MMPITeamRoleScale = apps.get_model('candidate_tests', 'MMPITeamRoleScale')
    MMPIScale = apps.get_model('candidate_tests', 'MMPIScale')
    values = testing_data_parser.parse_MMPI_team_role_scales()

    for v in values:
        role = MMPITeamRole.objects.get(name=v['role'])
        v.pop('role')
        scale = MMPIScale.objects.get(name=v['scale'])
        v.pop('scale')
        MMPITeamRoleScale.objects.update_or_create(role=role, scale=scale, **v)


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0026_auto_20210216_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='MMPITeamRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'ММИЛ командная роль',
                'verbose_name_plural': 'ММИЛ командные роли',
            },
        ),
        migrations.CreateModel(
            name='MMPITeamRoleScale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField()),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scales', to='candidate_tests.mmpiteamrole')),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='candidate_tests.mmpiscale')),
            ],
            options={
                'verbose_name': 'ММИЛ шкала командных ролей',
                'verbose_name_plural': 'ММИЛ шкалы командных ролей',
            },
        ),
        migrations.RunPython(MMPI_team_roles),
        migrations.RunPython(MMPI_team_role_scales),
    ]