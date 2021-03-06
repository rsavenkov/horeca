# Generated by Django 3.1.4 on 2021-03-03 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0034_mmpiusercompetence_mmpiusercompetencerecomendation'),
    ]

    operations = [
        migrations.CreateModel(
            name='MMPIUserStressTolerance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stress_tolerance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_stress_tolerances', to='candidate_tests.mmpistresstolerance')),
                ('testing_session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stress_tolerance', to='candidate_tests.testingsession')),
            ],
            options={
                'verbose_name': 'ММИЛ стрессоустойчивость пользователя',
                'verbose_name_plural': 'ММИЛ стрессоустойчивость пользователей',
            },
        ),
    ]
