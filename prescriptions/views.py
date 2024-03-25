from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Prescription
from .forms import PrescriptionForm,SearchForm

# def prescription_list(request):
#     prescriptions = Prescription.objects.all()
#     return render(request, 'prescriptions/prescription_list.html', {'prescriptions': prescriptions})

def prescription_list(request):
	search_form = SearchForm(request.GET)
	
	prescriptions = Prescription.objects.all()
	
	if search_form.is_valid():
		search_query = search_form.cleaned_data.get('search_query')
		search_by = search_form.cleaned_data.get('search_by')
		# if search_query:
		#     patients = patients.filter(patient__icontains=search_query)  # Example: Searching by name
		if search_query:
			if search_by == 'patient':
				prescriptions = prescriptions.filter(patient__name__icontains=search_query)
			elif search_by == 'id':
				prescriptions = prescriptions.filter(id=search_query)
			elif search_by == 'medication_name':
				prescriptions = prescriptions.filter(reason__icontains=search_query)

	context = {
		'prescriptions': prescriptions,
		'search_form': search_form,
	}

	return render(request,'prescriptions/prescription_list.html', context)


def prescription_detail(request, pk):
	prescriptions = get_object_or_404(Prescription, pk=pk)
	return render(request, 'prescriptions/prescription_detail.html', {'prescriptions': prescriptions})




def create_prescription(request):
	if request.method == 'POST':
		form = PrescriptionForm(request.POST)
		if form.is_valid():
			form.save()
			return prescription_list(request)
	else:
		form = PrescriptionForm()
	return render(request, 'prescriptions/prescription_form.html', {'form': form})
	#return render(request, 'prescriptions/create_prescription.html', {'form': form})


def update_prescription(request, pk):
	
	#prescription = Prescription.objects.get(id=prescription_id)
	prescription = get_object_or_404(Prescription, id=pk)

	if request.method == 'POST':
		form = PrescriptionForm(request.POST, instance=prescription)
		if form.is_valid():
			form.save()
			return prescription_list(request)
	else:
		form = PrescriptionForm(instance=prescription)
	
	return render(request, 'prescriptions/prescription_form.html', {'form': form})
	#return render(request, 'prescriptions/update_prescription.html', {'form': form})


# View for deleting an existing prescription
def delete_prescription(request, prescription_id):
	prescription = get_object_or_404(Prescription, id=prescription_id)
	if request.method == 'POST':
		prescription.delete()
		return prescription_list(request)  # Redirect to the list view after deleting the prescription
	return render(request, 'prescriptions/delete_prescription.html', {'prescription': prescription})
