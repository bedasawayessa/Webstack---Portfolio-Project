from django.contrib import admin

# Register your models here.
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'medication_name', 'dosage', 'start_date', 'end_date','updated_at']
    search_fields = ['patient__name', 'doctor__name']
    list_filter = ['medication_name', 'start_date', 'updated_at']
