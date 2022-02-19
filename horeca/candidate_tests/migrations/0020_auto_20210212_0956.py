# Generated by Django 3.1.4 on 2021-02-12 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0019_auto_20210211_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tpointstable',
            name='scale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t_points_tables', to='candidate_tests.mmpiscale'),
        ),
        migrations.CreateModel(
            name='MMPITestingUserTPointsResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.FloatField(default=0)),
                ('answer_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t_points', to='candidate_tests.mmpitestinguseranswerlist')),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='t_points', to='candidate_tests.mmpiscale')),
            ],
            options={
                'verbose_name': 'ММИЛ T-баллы пользователя',
                'verbose_name_plural': 'ММИЛ T-баллы пользователей',
                'unique_together': {('answer_list', 'scale')},
            },
        ),
    ]
