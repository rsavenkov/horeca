# Generated by Django 3.1.4 on 2021-02-26 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0029_testingsession_tests'),
    ]

    operations = [
        migrations.AddField(
            model_name='testingsession',
            name='status',
            field=models.CharField(choices=[('NOT_SEND', 'Не отправлено'), ('NOT_STARTED', 'Не начато'), ('IN_PROGRESS', 'В процессе'), ('NOT_COMPLETED', 'Не завершено'), ('COMPLETED', 'Завершено')], default='NOT_STARTED', max_length=100),
        ),
    ]
