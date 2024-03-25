from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.indexpage, name = "indexpage"),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/update/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('patient_report/', views.patient_report, name='patient_report'),
    path('individual_patient_report/<int:patient_id>/', views.individual_patient_report, name='individual_patient_report'),
    # Add more paths for creating, updating, and deleting patients
]