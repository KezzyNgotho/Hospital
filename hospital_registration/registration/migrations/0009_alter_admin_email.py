# Generated by Django 4.2.2 on 2023-07-21 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_remove_attendance_check_out_attendance_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]
