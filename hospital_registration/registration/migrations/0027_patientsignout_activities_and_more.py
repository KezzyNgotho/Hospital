# Generated by Django 4.2.2 on 2023-07-24 11:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0026_remove_patientsignout_activities_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientsignout',
            name='activities',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patientsignout',
            name='is_inpatient',
            field=models.BooleanField(default=False),
        ),
    ]
