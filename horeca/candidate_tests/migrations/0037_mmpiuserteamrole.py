# Generated by Django 3.1.4 on 2021-03-04 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0036_auto_20210303_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='MMPIUserTeamRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField(default=0)),
                ('team_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_team_roles', to='candidate_tests.mmpiteamrole')),
                ('testing_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_roles', to='candidate_tests.testingsession')),
            ],
            options={
                'verbose_name': 'ММИЛ командная роль пользователя',
                'verbose_name_plural': 'ММИЛ командные роли пользователей',
            },
        ),
    ]