from django.contrib import admin
from .models import Patient, Doctor, Department

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Department) 
