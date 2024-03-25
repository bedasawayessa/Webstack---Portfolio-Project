from django.urls import path
from . import views

app_name = 'prescriptions'

urlpatterns = [
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptionsform/', views.create_prescription, name='create_prescription'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('prescriptions/<int:pk>/update/', views.update_prescription, name='update_prescription'),
    path('prescriptions/<int:prescription_id>/delete/', views.delete_prescription, name='delete_prescription'),
   
    # Add more paths for creating, updating, and deleting prescriptions
]