# Generated by Django 3.1.4 on 2021-04-05 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0046_auto_20210323_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mmpitestinguserrawpointsresult',
            name='points',
            field=models.FloatField(default=0),
        ),
    ]
