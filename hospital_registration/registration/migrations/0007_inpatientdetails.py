# Generated by Django 4.2.2 on 2023-07-19 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_patient_patient_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='InpatientDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=100)),
                ('check_in', models.DateTimeField(auto_now_add=True)),
                ('incharge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.incharge')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.patient')),
            ],
        ),
    ]
