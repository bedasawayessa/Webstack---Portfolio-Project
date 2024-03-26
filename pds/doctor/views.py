from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Doctor
from .forms import DoctorForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def register_doctor(request):
    user_role = 'doctor'  # Define the user role to filter (e.g., 'admin', 'doctor', 'patient', etc.)
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            form = DoctorForm(request.POST)
            if form.is_valid():
                form.save()
                return doctor_list(request)  # Redirect to a page showing the list of doctors
        else:
            form = DoctorForm(user_role=user_role)
        return render(request, 'doctor/doctor_form.html', {'form': form})
    else:
        return redirect('login_user')  # Redirect unauthorized users to the login page


@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    # Check if the user is an admin
    if request.user.is_authenticated and request.user.is_admin:
        # Admin can update all doctors
        if request.method == 'POST':
            form = DoctorForm(request.POST, instance=doctor)
            if form.is_valid():
                form.save()
                return doctor_list(request)
        else:
            form = DoctorForm(instance=doctor)
    else:
        # Check if the user is a doctor and can only update their own profile
        if request.user.is_authenticated and request.user.role == 'doctor' and doctor.user == request.user:
            if request.method == 'POST':
                form = DoctorForm(request.POST, instance=doctor)
                if form.is_valid():
                    form.save()
                    return redirect('doctor:doctor_detail', pk=pk)  # Redirect to the doctor detail page
            else:
                form = DoctorForm(instance=doctor)
        else:
            messages.error(request, "You can only edit your own profile.")
            return doctor_list(request)
            #return redirect('users:login_user')

    return render(request, 'doctor/doctor_form.html', {'form': form})
# def doctor_update(request, pk):
#     doctor = get_object_or_404(Doctor, pk=pk)
#     if request.method == 'POST':
#         form = DoctorForm(request.POST, instance=doctor)
#         if form.is_valid():
#             form.save()
#             return doctor_list(request)
#     else:
#         form = DoctorForm(instance=doctor)
#     return render(request, 'doctor/doctor_form.html', {'form': form})


# def doctor_list(request):
#     doctors = Doctor.objects.all()
#     return render(request, 'doctor/doctor_list.html', {'doctors': doctors})
@login_required
def doctor_list(request):
    search_form = SearchForm(request.GET)
    doctors = Doctor.objects.all().order_by('-id')
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        search_by = search_form.cleaned_data.get('search_by')
        # if search_query:
        #     patients = patients.filter(name__icontains=search_query)  # Example: Searching by name

        if search_query:
            if search_by == 'name':
                doctors = doctors.filter(name__icontains=search_query)
            elif search_by == 'id':
                doctors = doctors.filter(id=search_query)
            elif search_by == 'specialty':
                doctors = doctors.filter(specialty__icontains=search_query)

    context = {
        'doctors': doctors,
        'search_form': search_form,
    }

    return render(request, 'doctor/doctor_list.html', context)
@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctor/doctor_detail.html', {'doctor': doctor})
