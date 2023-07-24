# Generated by Django 4.2.2 on 2023-07-21 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_alter_admin_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='signed_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patientsignout',
            name='is_inpatient',
            field=models.BooleanField(default=False),
        ),
    ]
