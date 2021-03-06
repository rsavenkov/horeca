# Generated by Django 3.1.4 on 2021-03-10 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0040_nonverballogicansweroption_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogicTestResultDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(choices=[('NUMERIC_LOGIC', 'NUMERIC_LOGIC'), ('VERBAL_LOGIC', 'VERBAL_LOGIC'), ('NON_VERBAL_LOGIC', 'NON_VERBAL_LOGIC')], max_length=100)),
                ('result', models.CharField(choices=[('HIGHT', 'HIGHT'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW')], max_length=100)),
                ('from_point', models.PositiveIntegerField()),
                ('to_point', models.PositiveIntegerField()),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Описание логического теста',
                'verbose_name_plural': 'Описания логических тестов',
            },
        ),
        migrations.AlterField(
            model_name='nonverballogicuseranswerlist',
            name='result',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='numericlogicuseranswerlist',
            name='result',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='verballogicuseranswerlist',
            name='result',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
