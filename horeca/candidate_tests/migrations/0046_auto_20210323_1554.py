# Generated by Django 3.1.4 on 2021-03-23 15:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0045_mmpiscale_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profinterestsresult',
            name='points',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
