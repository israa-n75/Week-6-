
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, Department


# Home page - login illatheyum kaanam
def home(request):
    return render(request, 'home.html')


# View all patients
@login_required(login_url='login')
def patients(request):
    patient_list = Patient.objects.all()
    return render(request, 'patients.html', {
        'patients': patient_list
    })


# Add a patient
@login_required(login_url='login')
def add_patient(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        disease = request.POST.get("disease")

        Patient.objects.create(
            name=name,
            age=age,
            disease=disease
        )
        return redirect('patients')

    return render(request, 'add_patient.html')


# Edit a patient
@login_required(login_url='login')
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        patient.name = request.POST.get("name")
        patient.age = request.POST.get("age")
        patient.disease = request.POST.get("disease")
        patient.save()
        return redirect('patients')

    return render(request, 'edit_patient.html', {
        'patient': patient
    })


# Delete a patient
@login_required(login_url='login')
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        patient.delete()

    return redirect('patients')


# View all doctors
@login_required(login_url='login')
def doctors(request):
    doctor_list = Doctor.objects.all()
    return render(request, 'doctors.html', {
        'doctors': doctor_list
    })


# Add a doctor
@login_required(login_url='login')
def add_doctor(request):
    if request.method == "POST":
        name = request.POST.get("name")
        specialization = request.POST.get("specialization")
        age = request.POST.get("age")

        Doctor.objects.create(
            name=name,
            specialization=specialization,
            age=age
        )
        return redirect('doctors')

    return render(request, 'add_doctor.html')


# Edit a doctor
@login_required(login_url='login')
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        doctor.name = request.POST.get("name")
        doctor.specialization = request.POST.get("specialization")
        doctor.age = request.POST.get("age")
        doctor.save()
        return redirect('doctors')

    return render(request, 'edit_doctor.html', {
        'doctor': doctor
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
    department_list = Department.objects.all()

    return render(request, 'departments.html', {
        'departments': department_list
    })


# Add a department
@login_required(login_url='login')
def add_department(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        Department.objects.create(
            name=name,
            description=description
        )
        return redirect('departments')

    return render(request, 'add_department.html')


# Edit a department
@login_required(login_url='login')
def edit_department(request, department_id):
    department = get_object_or_404(
        Department, id=department_id
    )

    if request.method == "POST":
        department.name = request.POST.get("name")
        department.description = request.POST.get("description")
        department.save()
        return redirect('departments')

    return render(request, 'edit_department.html', {
        'department': department
    })


# Delete a department
@login_required(login_url='login')
def delete_department(request, department_id):
    department = get_object_or_404(
        Department, id=department_id
    )

    if request.method == "POST":
        department.delete()

    return redirect('departments')


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
