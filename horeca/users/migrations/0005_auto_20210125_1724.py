# Generated by Django 3.1.4 on 2021-01-25 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210122_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('patronymic', models.CharField(blank=True, max_length=150, verbose_name='patronymic')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Администратор',
                'verbose_name_plural': 'Администраторы',
            },
        ),
        migrations.CreateModel(
            name='CandidateCreator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.admin')),
                ('manager', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.manager')),
            ],
            options={
                'verbose_name': 'Создатель кандидата',
                'verbose_name_plural': 'Создатели кандидата',
            },
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='manager',
        ),
        migrations.DeleteModel(
            name='Administrator',
        ),
        migrations.AddField(
            model_name='candidate',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='candidates', to='users.candidatecreator'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='candidatecreator',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('admin__isnull', False), ('manager__isnull', True)), models.Q(('admin__isnull', True), ('manager__isnull', False)), _connector='OR'), name='only_one_not_null'),
        ),
    ]
