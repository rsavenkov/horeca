# Generated by Django 3.1.4 on 2021-03-22 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_candidate_testing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='city',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
