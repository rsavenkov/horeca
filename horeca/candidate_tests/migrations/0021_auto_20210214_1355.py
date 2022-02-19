# Generated by Django 3.1.4 on 2021-02-14 13:55

from django.db import migrations, models

from candidate_tests.utils import constants, testing_data_parser


def MMPI_questions(apps, schema_editor):
    MMPIQuestion = apps.get_model('candidate_tests', 'MMPIQuestion')
    questions = testing_data_parser.parse_MMPI_questions_file('MMPI_questions.csv')

    for q in questions:
        MMPIQuestion.objects.update_or_create(
            number=q['id'],
            question=q['question'],
        )


def MMPI_scales(apps, schema_editor):
    MMPIScale = apps.get_model('candidate_tests', 'MMPIScale')
    scales = testing_data_parser.parse_json_file('MMPI_scales.json')
    for s in constants.MMPIScales:
        scale_info = scales[s.value]
        scale, _ = MMPIScale.objects.get_or_create(name=s.value)
        scale.is_inverted = scale_info.get('is_inverted', False)
        scale.verbose_name = scale_info['verbose_name']
        scale.negative_keys.add(*scale_info['negative_keys'])
        scale.positive_keys.add(*scale_info['positive_keys'])
        scale.save()


def MMPI_T_points(apps, schema_editor):
    TPointsTable = apps.get_model('candidate_tests', 'TPointsTable')
    MMPIScale = apps.get_model('candidate_tests', 'MMPIScale')
    points = testing_data_parser.parse_json_file('MMPI_T_points.json')

    for s in constants.MMPIScales:
        scale = MMPIScale.objects.get(name=s.value)
        point = points[scale.name]

        for key in point:
            table, _ = TPointsTable.objects.get_or_create(
                scale=scale,
                gender=constants.Genders.MALE.value if key == 'male' else constants.Genders.FEMALE.value,
            )
            table.m = point[key]['m']
            table.delta = point[key]['delta']
            table.save()

class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0020_auto_20210212_0956'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tpointstable',
            options={'verbose_name': 'ММИЛ Tаблица T-баллов', 'verbose_name_plural': 'ММИЛ Таблицы T-баллов'},
        ),
        migrations.AlterField(
            model_name='mmpitestinguserrawpointsresult',
            name='points',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='tpointstable',
            name='delta',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='tpointstable',
            name='m',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='mmpiscale',
            name='verbose_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.RunPython(MMPI_questions),
        migrations.RunPython(MMPI_scales),
        migrations.RunPython(MMPI_T_points),
    ]
