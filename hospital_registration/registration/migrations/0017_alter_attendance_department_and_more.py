# Generated by Django 4.2.2 on 2023-07-23 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_alter_patientsignout_incharge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='room_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
