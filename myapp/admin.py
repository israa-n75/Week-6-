from django.contrib import admin
from .models import Patient, Doctor, Department, MedicalRecord, Treatment, Profile

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Department)
admin.site.register(MedicalRecord)
admin.site.register(Treatment)
admin.site.register(Profile)