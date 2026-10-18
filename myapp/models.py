from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name