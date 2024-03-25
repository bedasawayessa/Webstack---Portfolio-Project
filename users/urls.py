# urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('accounts/login/', views.login_user, name='login_user'),
    path('accounts/logout/', views.logoutpage, name='logoutpage'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('users_list', views.users_list, name='users_list'),
    path('users/<int:pk>/', views.users_detail, name='users_detail'),
    path('update_user/<int:pk>/update/', views.user_update, name='user_update'),
    path('delete_user/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    
    
    # Add more paths for login, profile management, etc.
]