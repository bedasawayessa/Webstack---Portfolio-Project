from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('register_doctor/', views.register_doctor, name='register_doctor'),
    path('doctor/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    
    # Add more paths for creating, updating, and deleting appointments
]