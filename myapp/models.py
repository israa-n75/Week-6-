from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    disease = models.CharField(max_length=100, default="")

    # One Doctor → Many Patients
    doctor = models.ForeignKey(
        'Doctor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients"
    )

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)

    # Keeping the existing field for now
    doctor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    age = models.IntegerField()

    # One Department → Many Doctors
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctors"
    )

    def __str__(self):
        return self.name


class MedicalRecord(models.Model):
    # One Patient → Many Medical Records
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="medical_records"
    )

    diagnosis = models.CharField(max_length=200)
    record_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.name} - {self.diagnosis}"


class Treatment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    patients = models.ManyToManyField(
        Patient,
        related_name="treatments",
        blank=True
    )

    def __str__(self):
        return self.name


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    avatar = models.ImageField(upload_to='profile_avatars/', blank=True, null=True)

    bio = models.TextField(blank=True)

    phone = models.CharField(max_length=15,blank=True)

    def __str__(self):
        return self.user.username