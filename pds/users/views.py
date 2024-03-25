from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import UserRegistrationForm, UserLoginForm,SearchForm, UserChangeForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .decorators import admin_required


# views.py continued

# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Additional logic to handle different roles
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'users/register.html', {'form': form})

# @admin_required
@login_required
def register_user(request):
	user_role = 'admin'  # Define the user role to filter (e.g., 'admin', 'doctor', 'patient', etc.)
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)  # Save the form data without committing to the database
			role = form.cleaned_data.get('role')  # Get the selected role from the form
			user.role = role
			user.save()

			# Additional logic to handle different roles if needed
			# Additional logic to handle different roles
			if role == 'admin':
				# Perform actions specific to admin role
				user.is_staff = True
				user.is_superuser = True
			elif role == 'doctor':
				user.is_staff = True
			elif role == 'patient':
				user.is_staff = True
			return login_user(request)
			
	else:
		form = UserRegistrationForm(user_role=user_role)
	
	return render(request, 'users/users_form.html', {'form': form})

def user_update(request, pk):
	
	user = get_object_or_404(CustomUser, pk = pk)

	if request.method == 'POST':
		print("New Received POST data:", request.POST)
		form = UserRegistrationForm(request.POST, instance=user)
		#form = UserRegistrationForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			return users_list(request)  # Redirect to the user's profile page after successful update
		
	else:
		form = UserRegistrationForm(instance=user)

	return render(request, 'users/users_form.html', {'form': form,'user': user})

def login_user(request):
	if request.POST:
		form = UserLoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			print(f"email={email} password={password}")
			user = authenticate(request, email=email, password=password)		
			print(f"email={email} password={password}")
			if user is not None:
				print(f"User: email={user.email} password={user.password}")
				login(request, user)
			
				user_type = get_user_type(user)
				if user_type == 'admin':
					#return redirect('student_dashboard')
					request.session['user_type'] = 'admin'
					#return render(request, 'back/student/profile.html', {'user': request.user})
					return redirect("users:admin_dashboard")
					#return student_profile(request)
				if user_type == 'patient':
					#return redirect('student_dashboard')
					request.session['user_type'] = 'patient'
					#return render(request, 'back/student/profile.html', {'user': request.user})
					return redirect("users:patient_dashboard")
					#return student_profile(request)
				if user_type == 'doctor':
					#return redirect('student_dashboard')
					request.session['user_type'] = 'doctor'
					#return render(request, 'back/student/profile.html', {'user': request.user})
					return redirect("users:doctor_dashboard")
				
				# else:
				# 	return redirect('patients:indexpage')  # Redirect users with unknown roles to the home page
			else:
				form.add_error(None, 'Invalid email or password. Please try again.')
		else:
			form.add_error(None, 'Invalid form submission. Please check the form data.')
	else:
		form = UserLoginForm()
	
	return render(request, 'users/login.html', {'form': form})

# Helper function to get user type
def get_user_type(user):
	try:
		#user_info = User.objects.get(user=user)
		user_info = CustomUser.objects.get(pk=user.pk)		
		print(f"The type of user is: {user_info.role}")
		return user_info.role
	except CustomUser.DoesNotExist:
		# Handle the case where the user profile does not exist
		return None

@login_required
def logoutpage(request):
	if request.user.is_authenticated:
		logout(request)
		request.session.flush()  # Destroy the session
		return render(request, 'front/logout.html')
	else:
		return render(request, 'front/login.html') 


def users_list(request):
	search_form = SearchForm(request.GET)
	users = CustomUser.objects.all().order_by('-id')
	if search_form.is_valid():
		search_query = search_form.cleaned_data.get('search_query')
		search_by = search_form.cleaned_data.get('search_by')
		# if search_query:
		#     patients = patients.filter(name__icontains=search_query)  # Example: Searching by name

		if search_query:
			if search_by == 'name':
				users = users.filter(name__icontains=search_query)
			elif search_by == 'id':
				users = users.filter(id=search_query)
			elif search_by == 'role':
				users = users.filter(role__icontains=search_query)

	context = {
		'users': users,
		'search_form': search_form,
	}

	return render(request, 'users/users_list.html', context)


def users_detail(request, pk):
	users = get_object_or_404(CustomUser, pk=pk)
	return render(request, 'back/users_detail.html', {'users': users})
@login_required(login_url='/accounts/login/')
def admin_dashboard(request):
	return render(request, 'back/admin_dashboard.html')


@login_required(login_url='/accounts/login/')
def doctor_dashboard(request):
	return render(request, 'back/doctor_dashboard.html')


@login_required(login_url='/accounts/login/')
def patient_dashboard(request):
	return render(request, 'back/patient_dashboard.html')

# @login_required(login_url='/accounts/login/')
# def user_update(request, pk):
# 	instance = get_object_or_404(CustomUser, pk=pk)
# 	if request.method == 'POST':
# 		form = UserUpdateForm(request.POST, pk=instance)
# 		#form = UserRegistrationForm(request.POST, instance=instance)
# 		if form.is_valid():
# 			#form.save()
# 			form.update_user_instance(instance)
# 			return users_list(request)
# 	else:
# 		form = UserUpdateForm(instance=instance)
# 		#form = UserRegistrationForm(instance=instance)
# 	return render(request, 'users/users_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def user_delete(request, pk):
	users = get_object_or_404(CustomUser, pk=pk)
	if request.method == 'POST':
		users.delete()
		return users_list(request)
	return render(request, 'users/user_confirm_delete.html', {'users': users})


# def role_based_dashboard(request):
#     user = request.user
#     if user.is_authenticated:
#         if user.role == 'admin':
#             return redirect('admin_dashboard')
#         elif user.role == 'doctor':
#             return redirect('doctor_dashboard')
#         elif user.role == 'patient':
#             return redirect('patient_dashboard')
#     # Handle other roles or unauthenticated users
#     return redirect('login')  # Redirect to login page if role is not defined