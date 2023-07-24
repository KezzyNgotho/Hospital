from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class MyModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    # Other fields and methods
    # Add other fields as required


class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, default="adminkezz@gmail.com")
    # email = models.EmailField(max_length=100, unique=True, default='adminkezz@gmail.com')
    # Other fields...

    # Add other fields as required

    @classmethod
    def can_create(cls):
        return cls.objects.count() < 5


class Incharge(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    # Add other fields as required

    @classmethod
    def can_create(cls):
        return cls.objects.count() < 4

    # Add other fields as required




class Patient(models.Model):
    INPATIENT = 'inpatient'
    OUTPATIENT = 'outpatient'

    PATIENT_TYPE_CHOICES = [
        (INPATIENT, 'Inpatient'),
        (OUTPATIENT, 'Outpatient'),
    ]

    student_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    patient_type = models.CharField(max_length=20, choices=PATIENT_TYPE_CHOICES)

    def __str__(self):
        return self.full_name
    
# models.py
class Attendance(models.Model):
    INPATIENT = 'inpatient'
    OUTPATIENT = 'outpatient'
    PATIENT_TYPE_CHOICES = [
        (INPATIENT, 'Inpatient'),
        (OUTPATIENT, 'Outpatient'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    incharge = models.ForeignKey(Incharge, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    room_number = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    patient_type = models.CharField(max_length=20, choices=PATIENT_TYPE_CHOICES)  # New field for patient type
    student_number = models.CharField(max_length=20)  # New field for student number

    # ... other fields and methods ...

    # Add other fields as required


class InpatientDetails(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    incharge = models.ForeignKey(Incharge, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)

    # Add any additional fields and methods as per your requirements

    def __str__(self):
        return f"Inpatient Details for {self.patient.full_name}"

    # Add other fields as required


# models.py


# ... Your other view functions ...


class PatientSignOut(models.Model):
    check_in = models.DateTimeField()
    incharge = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    is_inpatient = models.BooleanField(default=False)  # New field

    class Meta:
        unique_together = (("check_in", "incharge", "patient"),)

    def save(self, *args, **kwargs):
        self.is_inpatient = self.patient.is_inpatient()
        super().save(*args, **kwargs)

# ... Your other view functions ...
