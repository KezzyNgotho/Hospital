# Generated by Django 4.2.2 on 2023-07-22 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0014_alter_patient_full_name_alter_patient_patient_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientsignout',
            name='incharge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.incharge'),
        ),
    ]
