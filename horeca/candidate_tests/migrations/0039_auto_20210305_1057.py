# Generated by Django 3.1.4 on 2021-03-05 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0038_auto_20210304_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='profinterestsresult',
            name='testing_session',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='prof_interests', to='candidate_tests.testingsession'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profinterestsresult',
            name='scale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_prof_interests', to='candidate_tests.profinterestsscale'),
        ),
        migrations.AlterUniqueTogether(
            name='profinterestsresult',
            unique_together={('testing_session', 'scale')},
        ),
        migrations.RemoveField(
            model_name='profinterestsresult',
            name='answer_list',
        ),
    ]
