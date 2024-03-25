from django.contrib import admin

# Register your models here.
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'time', 'created_at', 'updated_at']
    search_fields = ['patient__name']
    list_filter = ['time', 'created_at', 'updated_at']
