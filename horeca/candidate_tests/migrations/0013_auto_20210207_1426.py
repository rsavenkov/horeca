# Generated by Django 3.1.4 on 2021-02-07 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0012_auto_20210206_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfInterestsAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
            ],
            options={
                'verbose_name': 'Проф. интересы вариант ответа',
                'verbose_name_plural': 'Проф. интересы варианты ответов',
            },
        ),
        migrations.CreateModel(
            name='ProfInterestsQuestion',
            fields=[
                ('number', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('question', models.TextField()),
                ('points', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Проф. интересы вопрос',
                'verbose_name_plural': 'Проф. интересы вопросы',
            },
        ),
        migrations.CreateModel(
            name='ProfInterestsScale',
            fields=[
                ('number', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Проф. интересы шкала',
                'verbose_name_plural': 'Проф. интересы шкалы',
            },
        ),
        migrations.CreateModel(
            name='ProfInterestsUserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField()),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate_tests.profinterestsanswer')),
            ],
            options={
                'verbose_name': 'Проф. интересы ответ пользователья',
                'verbose_name_plural': 'Проф. интересы ответы пользователей',
            },
        ),
        migrations.AlterField(
            model_name='testingsessionstate',
            name='state',
            field=models.CharField(choices=[('PENDING_START', 'PENDING_START'), ('MMPI', 'MMPI'), ('NUMERIC_LOGIC', 'NUMERIC_LOGIC'), ('VERBAL_LOGIC', 'VERBAL_LOGIC'), ('NON_VERBAL_LOGIC', 'NON_VERBAL_LOGIC'), ('PROF_INTERESTS', 'PROF_INTERESTS')], default='PENDING_START', max_length=100),
        ),
        migrations.CreateModel(
            name='ProfInterestsUserAnswerList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ManyToManyField(through='candidate_tests.ProfInterestsUserAnswer', to='candidate_tests.ProfInterestsQuestion')),
                ('session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='prof_interests_user_answer_list', to='candidate_tests.testingsession')),
            ],
            options={
                'verbose_name': 'Проф. интересы список ответов пользователя',
                'verbose_name_plural': 'Проф. интересы списки ответов пользователей',
            },
        ),
        migrations.AddField(
            model_name='profinterestsuseranswer',
            name='answer_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='candidate_tests.profinterestsuseranswerlist'),
        ),
        migrations.AddField(
            model_name='profinterestsuseranswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='candidate_tests.profinterestsquestion'),
        ),
        migrations.AddField(
            model_name='profinterestsanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='candidate_tests.profinterestsquestion'),
        ),
        migrations.AddField(
            model_name='profinterestsanswer',
            name='scale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='candidate_tests.profinterestsscale'),
        ),
        migrations.AlterUniqueTogether(
            name='profinterestsuseranswer',
            unique_together={('answer_list', 'question', 'answer')},
        ),
    ]