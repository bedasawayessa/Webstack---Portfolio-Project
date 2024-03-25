# decorators.py
from functools import wraps
from django.shortcuts import redirect

# def admin_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         if request.user.is_authenticated and request.user.role == 'admin':
#             return view_func(request, *args, **kwargs)
#         else:
#             return redirect('users:login_user')  # Redirect unauthorized users to the login page
#     return _wrapped_view

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == role:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('users:login_user')  # Redirect unauthorized users to the login page
        return _wrapped_view
    return decorator

admin_required = role_required('admin')
doctor_required = role_required('doctor')