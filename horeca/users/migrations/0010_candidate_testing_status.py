# Generated by Django 3.1.4 on 2021-03-19 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210301_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='testing_status',
            field=models.CharField(choices=[('NOT_SEND', 'NOT_SEND'), ('RESEND', 'RESEND'), ('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('NOT_COMPLETED', 'NOT_COMPLETED'), ('COMPLETED', 'COMPLETED')], default='NOT_SEND', max_length=100),
        ),
    ]
