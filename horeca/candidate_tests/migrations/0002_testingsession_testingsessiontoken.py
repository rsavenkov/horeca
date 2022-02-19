# Generated by Django 3.1.4 on 2021-01-28 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210125_1724'),
        ('candidate_tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestingSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('token_ttl', models.DateTimeField(blank=True, null=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_sessions', to='users.candidate')),
            ],
            options={
                'verbose_name': 'Сессия тестирования',
                'verbose_name_plural': 'Сессии тестирования',
            },
        ),
        migrations.CreateModel(
            name='TestingSessionToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='session', to='candidate_tests.testingsession')),
            ],
            options={
                'verbose_name': 'Токен для прохождения тестирования',
                'verbose_name_plural': 'Токены для прохождения тестирования',
            },
        ),
    ]