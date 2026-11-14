
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models.deletion import ProtectedError

from .models import (
    Patient, Doctor, Department,
    MedicalRecord, Treatment, Profile
)


# Home page
def home(request):
    return render(request, 'home.html')


# View all patients
@login_required(login_url='login')
def patients(request):
    patient_list = Patient.objects.prefetch_related(
        'treatments'
    ).select_related('doctor').all()

    return render(request, 'patients.html', {
        'patients': patient_list
    })


# Add a patient
@login_required(login_url='login')
def add_patient(request):
    doctor_list = Doctor.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        disease = request.POST.get("disease")
        doctor_id = request.POST.get("doctor")

        doctor = None

        if doctor_id:
            doctor = get_object_or_404(Doctor, id=doctor_id)

        Patient.objects.create(
            name=name,
            age=age,
            disease=disease,
            doctor=doctor
        )

        return redirect('patients')

    return render(request, 'add_patient.html', {
        'doctors': doctor_list
    })


# Edit a patient
@login_required(login_url='login')
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctor_list = Doctor.objects.all()

    if request.method == "POST":
        patient.name = request.POST.get("name")
        patient.age = request.POST.get("age")
        patient.disease = request.POST.get("disease")

        doctor_id = request.POST.get("doctor")

        if doctor_id:
            patient.doctor = get_object_or_404(
                Doctor,
                id=doctor_id
            )
        else:
            patient.doctor = None

        patient.save()

        return redirect('patients')

    return render(request, 'edit_patient.html', {
        'patient': patient,
        'doctors': doctor_list
    })


# Delete a patient
@login_required(login_url='login')
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        try:
            patient.delete()
        except ProtectedError:
            messages.error(
                request,
                "Cannot delete this patient because medical records exist."
            )

    return redirect('patients')


# View all doctors
@login_required(login_url='login')
def doctors(request):
    doctor_list = Doctor.objects.select_related(
        'department'
    ).all()

    return render(request, 'doctors.html', {
        'doctors': doctor_list
    })


# Add a doctor
@login_required(login_url='login')
def add_doctor(request):
    department_list = Department.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        specialization = request.POST.get("specialization")
        age = request.POST.get("age")
        department_id = request.POST.get("department")

        department = None

        if department_id:
            department = get_object_or_404(
                Department,
                id=department_id
            )

        Doctor.objects.create(
            name=name,
            specialization=specialization,
            age=age,
            department=department
        )

        return redirect('doctors')

    return render(request, 'add_doctor.html', {
        'departments': department_list
    })


# Edit a doctor
@login_required(login_url='login')
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    department_list = Department.objects.all()

    if request.method == "POST":
        doctor.name = request.POST.get("name")
        doctor.specialization = request.POST.get("specialization")
        doctor.age = request.POST.get("age")

        department_id = request.POST.get("department")

        if department_id:
            doctor.department = get_object_or_404(
                Department,
                id=department_id
            )
        else:
            doctor.department = None

        doctor.save()

        return redirect('doctors')

    return render(request, 'edit_doctor.html', {
        'doctor': doctor,
        'departments': department_list
    })


# Delete a doctor
@login_required(login_url='login')
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        doctor.delete()

    return redirect('doctors')


# View all departments
@login_required(login_url='login')
def departments(request):
    department_list = Department.objects.prefetch_related(
        'doctors'
    ).all()

    return render(request, 'departments.html', {
        'departments': department_list
    })


# Add a department
@login_required(login_url='login')
def add_department(request):
    if request.method == "POST":
        name = request.POST.get("name")
        doctor_name = request.POST.get("doctor_name")

        Department.objects.create(
            name=name,
            doctor_name=doctor_name
        )

        return redirect('departments')

    return render(request, 'add_department.html')


# Edit a department
@login_required(login_url='login')
def edit_department(request, department_id):
    department = get_object_or_404(
        Department,
        id=department_id
    )

    if request.method == "POST":
        department.name = request.POST.get("name")
        department.doctor_name = request.POST.get("doctor_name")
        department.save()

        return redirect('departments')

    return render(request, 'edit_department.html', {
        'department': department
    })


# Delete a department
@login_required(login_url='login')
def delete_department(request, department_id):
    department = get_object_or_404(
        Department,
        id=department_id
    )

    if request.method == "POST":
        department.delete()

    return redirect('departments')


# NEW FEATURE 1:
# View all patients assigned to a specific doctor
@login_required(login_url='login')
def doctor_patients(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    patient_list = doctor.patients.all()

    return render(request, 'doctor_patients.html', {
        'doctor': doctor,
        'patients': patient_list
    })


# NEW FEATURE 2:
# Filter doctors by department name
@login_required(login_url='login')
def cardiology_doctors(request):
    doctor_list = Doctor.objects.filter(
        department__name__iexact='Cardiology'
    ).select_related('department')

    return render(request, 'cardiology_doctors.html', {
        'doctors': doctor_list
    })


# View medical records of a patient
@login_required(login_url='login')
def medical_records(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    records = patient.medical_records.all().order_by('-record_date')

    return render(request, 'medical_records.html', {
        'patient': patient,
        'records': records
    })


# Add a medical record
@login_required(login_url='login')
def add_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis", "").strip()
        notes = request.POST.get("notes", "").strip()

        if diagnosis:
            MedicalRecord.objects.create(
                patient=patient,
                diagnosis=diagnosis,
                notes=notes
            )

            return redirect(
                'medical_records',
                patient_id=patient.id
            )

        return render(request, 'add_medical_record.html', {
            'patient': patient,
            'error': 'Diagnosis is required!'
        })

    return render(request, 'add_medical_record.html', {
        'patient': patient
    })


# Edit a Medical Record
@login_required(login_url='login')
def edit_medical_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)

    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis", "").strip()
        notes = request.POST.get("notes", "").strip()

        if diagnosis:
            record.diagnosis = diagnosis
            record.notes = notes
            record.save()

            return redirect(
                'medical_records',
                patient_id=record.patient_id
            )

        return render(request, 'edit_medical_record.html', {
            'record': record,
            'patient': record.patient,
            'error': 'Diagnosis is required!'
        })

    return render(request, 'edit_medical_record.html', {
        'record': record,
        'patient': record.patient
    })


# Delete a Medical Record
@login_required(login_url='login')
def delete_medical_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)

    patient_id = record.patient_id

    if request.method == "POST":
        record.delete()

    return redirect(
        'medical_records',
        patient_id=patient_id
    )


# View all Treatments
@login_required(login_url='login')
def treatments(request):
    treatment_list = Treatment.objects.prefetch_related(
        'patients'
    ).all()

    return render(request, 'treatments.html', {
        'treatments': treatment_list
    })


# Add a Treatment
@login_required(login_url='login')
def add_treatment(request):
    patient_list = Patient.objects.all()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "")
        patient_ids = request.POST.getlist("patients")

        if name:
            treatment = Treatment.objects.create(
                name=name,
                description=description
            )

            selected_patients = Patient.objects.filter(
                id__in=patient_ids
            )

            treatment.patients.set(selected_patients)

            return redirect('treatments')

    return render(request, 'add_treatment.html', {
        'patients': patient_list
    })


# Edit Treatment
@login_required(login_url='login')
def edit_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    patient_list = Patient.objects.all()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "")
        patient_ids = request.POST.getlist("patients")

        if name:
            treatment.name = name
            treatment.description = description
            treatment.save()

            selected_patients = Patient.objects.filter(
                id__in=patient_ids
            )

            treatment.patients.set(selected_patients)

            return redirect('treatments')

    return render(request, 'edit_treatment.html', {
        'treatment': treatment,
        'patients': patient_list
    })


# Delete Treatment
@login_required(login_url='login')
def delete_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)

    if request.method == "POST":
        treatment.delete()

    return redirect('treatments')


# User Profile
@login_required(login_url='login')
def user_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        profile.bio = request.POST.get("bio", "").strip()
        profile.phone = request.POST.get("phone", "").strip()

        avatar = request.FILES.get("avatar")

        if avatar:
            profile.avatar = avatar

        profile.save()

        return redirect('profile')

    return render(request, 'profile.html', {
        'profile': profile
    })


# User login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('patients')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


# User logout
@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('home')
