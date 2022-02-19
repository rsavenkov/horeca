# Generated by Django 3.1.4 on 2021-01-30 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210125_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='date_of_birth',
            field=models.DateField(blank=True, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='gender',
            field=models.CharField(blank=True, choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')], max_length=50),
        ),
    ]