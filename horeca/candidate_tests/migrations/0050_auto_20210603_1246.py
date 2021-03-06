# Generated by Django 3.1.4 on 2021-06-03 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0049_auto_20210603_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonverballogicuseranswer',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate_tests.nonverballogicanswer'),
        ),
        migrations.AlterField(
            model_name='numericlogicuseranswer',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate_tests.numericlogicanswer'),
        ),
        migrations.AlterField(
            model_name='verballogicuseranswer',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate_tests.verballogicanswer'),
        ),
    ]
