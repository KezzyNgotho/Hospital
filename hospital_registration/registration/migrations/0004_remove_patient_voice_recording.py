# Generated by Django 4.2.2 on 2023-07-19 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_rename_name_patient_full_name_remove_patient_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='voice_recording',
        ),
    ]