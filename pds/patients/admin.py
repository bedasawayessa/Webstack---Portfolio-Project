from django.contrib import admin

# Register your models here.
from .models import Patient

from .models import Patient
from patients.forms import PatientForm

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    form = PatientForm
    list_display = ['id', 'name', 'medical_history', 'created_at']
    search_fields = ['name']
    list_filter = ['gender', 'name']