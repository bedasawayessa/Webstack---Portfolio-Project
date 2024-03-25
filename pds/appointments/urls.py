from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
   
    # Add more paths for creating, updating, and deleting appointments
]