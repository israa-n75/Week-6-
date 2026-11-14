
from django.contrib import admin
from django.urls import path,include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    

    # Patients
    path('patients/', views.patients, name='patients'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('edit_patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('doctor/<int:doctor_id>/patients/',views.doctor_patients,name='doctor_patients'),

    # Doctors
    path('doctors/', views.doctors, name='doctors'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('edit_doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('cardiology-doctors/',views.cardiology_doctors,name='cardiology_doctors'),

    # Departments
    path('departments/', views.departments, name='departments'),
    path('add_department/', views.add_department, name='add_department'),
    path('edit_department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),

    # Medical Records
    path('patients/<int:patient_id>/medical-records/',views.medical_records,name='medical_records'),
    path('patients/<int:patient_id>/medical-records/add/',views.add_medical_record,name='add_medical_record'),
    path('medical-records/<int:record_id>/edit/',views.edit_medical_record,name='edit_medical_record'),  
    path('medical-records/<int:record_id>/delete/',views.delete_medical_record,name='delete_medical_record'),
    
    # Treatments
    path('treatments/', views.treatments, name='treatments'),
    path('add_treatment/', views.add_treatment, name='add_treatment'),
    path('edit_treatment/<int:treatment_id>/',views.edit_treatment,name='edit_treatment'),
    path( 'delete_treatment/<int:treatment_id>/',views.delete_treatment,name='delete_treatment' ),
    path('profile/', views.user_profile, name='profile'),

    
    # Login
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

if settings.DEBUG:    
    urlpatterns += [        
        path('__debug__/', 
        include('debug_toolbar.urls')),    
    ]
