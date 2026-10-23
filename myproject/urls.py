from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),  

    path('admin/', admin.site.urls),

    # Patients
    path('patients/', views.patients, name='patients'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('edit_patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    # Doctors
    path('doctors/', views.doctors, name='doctors'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('edit_doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),

    # Departments
    path('departments/', views.departments, name='departments'),
    path('add_department/', views.add_department, name='add_department'),
    path('edit_department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),

    # Login
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]



