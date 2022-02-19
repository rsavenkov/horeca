# Generated by Django 3.1.4 on 2021-02-25 08:56

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_tests', '0028_mmpistresstolerance_mmpistresstolerancescale_mmpistresstolerancescalescombination'),
    ]

    operations = [
        migrations.AddField(
            model_name='testingsession',
            name='tests',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('MMPI', 'MMPI'), ('NUMERIC_LOGIC', 'NUMERIC_LOGIC'), ('VERBAL_LOGIC', 'VERBAL_LOGIC'), ('NON_VERBAL_LOGIC', 'NON_VERBAL_LOGIC'), ('PROF_INTERESTS', 'PROF_INTERESTS')], default=None, max_length=63),
            preserve_default=False,
        ),
    ]