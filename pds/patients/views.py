from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Patient
from prescriptions.models import Prescription
from appointments.models import Appointment

from django.db.models import Sum
from .forms import PatientForm
from .forms import SearchForm
from users.decorators import admin_required, doctor_required
from django.contrib.auth.decorators import login_required


def indexpage(request):
	return render(request, 'index.html')

def patient_list(request):
    search_form = SearchForm(request.GET)
    patients = Patient.objects.all().order_by('-id')
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        search_by = search_form.cleaned_data.get('search_by')
        # if search_query:
        #     patients = patients.filter(name__icontains=search_query)  # Example: Searching by name

        if search_query:
            if search_by == 'name':
                patients = patients.filter(name__icontains=search_query)
            elif search_by == 'id':
                patients = patients.filter(id=search_query)
            elif search_by == 'diagnosis':
                patients = patients.filter(medical_history__icontains=search_query)

    context = {
        'patients': patients,
        'search_form': search_form,
    }

    return render(request, 'patients/patient_list.html', context)
    #return render(request, 'patients/patient_list.html', {'patients': patients})


def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/patient_detail.html', {'patient': patient})

# @admin_required
# @doctor_required
@login_required
def patient_create(request):
    user_role = 'patient'  # Define the user role to filter (e.g., 'admin', 'doctor', 'patient', etc.)
    if request.method == 'POST':
        form = PatientForm( request.POST)
        if form.is_valid():
            form.save()
            return patient_list(request)
    else:
        form = PatientForm(user_role=user_role)
        #form.fields['username'].initial = request.user.username  # Populate the username 
    return render(request, 'patients/patient_form.html', {'form': form})
@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return patient_list(request)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return patient_list(request)
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})

def patient_report(request):
    # Get total number of patients
    total_patients = Patient.objects.count()

    # Get average age of patients
    total_age = Patient.objects.aggregate(total_age=Sum('age'))
    average_age = total_age['total_age'] / total_patients if total_patients > 0 else 0

    # Get total number of prescriptions
    total_prescriptions = Prescription.objects.count()

    # Get total number of appointments
    total_appointments = Appointment.objects.count()

    # Calculate revenue from prescriptions
    total_revenue = Prescription.objects.count() * 100  # Assuming each prescription costs $100

    context = {
        'total_patients': total_patients,
        'average_age': average_age,
        'total_prescriptions': total_prescriptions,
        'total_appointments': total_appointments,
        'total_revenue': total_revenue,
    }

    return render(request, 'patients/patient_report.html', context)


def individual_patient_report(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    prescriptions = Prescription.objects.filter(patient=patient)
    appointments = Appointment.objects.filter(patient=patient)
    
    context = {
        'patient': patient,
        'prescriptions': prescriptions,
        'appointments': appointments,
    }
    
    return render(request, 'patients/individual_patient_report.html', context)