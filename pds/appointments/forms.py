from django import forms
from .models import Doctor
from users.models import CustomUser

from .models import Appointment

class AppointmentForm(forms.ModelForm):
    
    time = forms.DateTimeField(widget=forms.SelectDateWidget())
    #created_at = forms.DateTimeField(widget=forms.SelectDateWidget())
   
    class Meta:
        model = Appointment
        fields = ['time', 'patient', 'doctor', 'reason']
        #fields = ['time', 'created_at', 'updated_at', 'patient', 'doctor', 'reason']
        # exclude = ['created_at', 'updated_at']
       

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', required=False)
    search_by = forms.ChoiceField(label='Search By', choices=[('patient', 'patient'), ('id', 'ID'), ('reason', 'reason')], required=False)