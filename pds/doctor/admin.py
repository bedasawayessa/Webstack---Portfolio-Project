from django.contrib import admin
from .models import Doctor
from doctor.forms import DoctorForm
# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    form = DoctorForm
    list_display = ['get_username','name', 'specialty']
    search_fields = ['user__username','name', 'specialty']

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'username'  # Display as 'Username' in the admin 
