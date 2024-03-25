from django.contrib import admin
from users.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_staff', 'is_admin', 'is_superuser','is_active']
    search_fields = ['role']
    list_filter = ['role', 'username']
