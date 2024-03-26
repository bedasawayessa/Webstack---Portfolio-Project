from django.shortcuts import render, redirect
from .forms import SearchForm

# Create your views here.
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required

@login_required
def appointment_list(request):
	search_form = SearchForm(request.GET)
	
	users = Appointment.objects.all().order_by('-id')
	
	if search_form.is_valid():
		search_query = search_form.cleaned_data.get('search_query')
		search_by = search_form.cleaned_data.get('search_by')
		# if search_query:
		#     patients = patients.filter(name__icontains=search_query)  # Example: Searching by name
		if search_query:
			if search_by == 'patient':
				users = users.filter(patient__name__icontains=search_query)
			elif search_by == 'id':
				users = users.filter(id=search_query)
			elif search_by == 'reason':
				users = users.filter(reason__icontains=search_query)

	context = {
		'users': users,
		'search_form': search_form,
	}

	return render(request, 'appointments/appointment_list.html', context)

	# appointments = Appointment.objects.all()
	# return render(request, 'appointments/appointment_list.html', {'appointments': appointments})



@login_required
def create_appointment(request):
	if request.method == 'POST':
		form = AppointmentForm(request.POST)
		if form.is_valid():
			form.save()
			return appointment_list(request)  # Redirect to appointment list page after successful creation
	else:
		form = AppointmentForm()
	return render(request, 'appointments/appointments_form.html', {'form': form})