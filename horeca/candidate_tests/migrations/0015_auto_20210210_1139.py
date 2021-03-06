# Generated by Django 3.1.4 on 2021-02-10 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0014_auto_20210206_2234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mmpitestinguseranswerlist',
            old_name='answers',
            new_name='questions',
        ),
        migrations.RenameField(
            model_name='nonverballogicuseranswerlist',
            old_name='answers',
            new_name='questions',
        ),
        migrations.RenameField(
            model_name='numericlogicuseranswerlist',
            old_name='answers',
            new_name='questions',
        ),
        migrations.RenameField(
            model_name='profinterestsuseranswerlist',
            old_name='answers',
            new_name='questions',
        ),
        migrations.RenameField(
            model_name='verballogicuseranswerlist',
            old_name='answers',
            new_name='questions',
        ),
        migrations.AlterField(
            model_name='mmpitestinguseranswer',
            name='answer_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='candidate_tests.mmpitestinguseranswerlist'),
        ),
        migrations.AlterField(
            model_name='nonverballogicuseranswer',
            name='answer_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='candidate_tests.nonverballogicuseranswerlist'),
        ),
        migrations.AlterField(
            model_name='numericlogicuseranswer',
            name='answer_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='candidate_tests.numericlogicuseranswerlist'),
        ),
        migrations.AlterField(
            model_name='profinterestsuseranswer',
            name='answer_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='candidate_tests.profinterestsuseranswerlist'),
        ),
        migrations.AlterField(
            model_name='testingsessionstate',
            name='state',
            field=models.CharField(choices=[('PENDING_START', 'PENDING_START'), ('MMPI', 'MMPI'), ('NUMERIC_LOGIC', 'NUMERIC_LOGIC'), ('VERBAL_LOGIC', 'VERBAL_LOGIC'), ('NON_VERBAL_LOGIC', 'NON_VERBAL_LOGIC'), ('PROF_INTERESTS', 'PROF_INTERESTS'), ('FINISH', 'FINISH')], default='PENDING_START', max_length=100),
        ),
        migrations.AlterField(
            model_name='verballogicuseranswer',
            name='answer_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='candidate_tests.verballogicuseranswerlist'),
        ),
    ]
