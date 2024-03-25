from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medication_name', 'dosage', 'frequency', 'start_date', 'end_date', 'doctor', ]

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', required=False)
    search_by = forms.ChoiceField(label='Search By', choices=[('patient', 'patient'), ('id', 'ID'), ('medication_name', 'medication_name')], required=False)