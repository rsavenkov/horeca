# Generated by Django 3.1.4 on 2021-05-27 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0047_auto_20210405_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mmpiuserleadershipstyle',
            name='value',
        ),
        migrations.AddField(
            model_name='mmpiuserleadershipstyle',
            name='type',
            field=models.CharField(choices=[('HIGHT', 'Характерно'), ('MEDIUM', 'Условно характерно'), ('LOW', 'Не характерно')], default='Не характерно', max_length=100),
            preserve_default=False,
        ),
    ]
