from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.contrib.auth.models import PermissionsMixin
from . managers import MyUserManager



# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
	
	email   = models.EmailField(help_text="Your Email must be unique.",verbose_name="email", max_length=60, unique=True)
	username = models.CharField(help_text="Your Username must be unique.", max_length=30, unique=True)
	name 	 = models.CharField(max_length=30)
	
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login	= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin	= models.BooleanField(default=False)
	is_active   = models.BooleanField(default=True)
	is_staff	= models.BooleanField(default=False)
	is_superuser= models.BooleanField(default=False)

	ROLES = (
        ('admin', 'admin'),
        ('doctor', 'doctor'),
        ('patient', 'patient'),
    )
	role = models.CharField(max_length=20, choices=ROLES)
	
	USERNAME_FIELD = "email"
	EMAIL_FIELD = "email"
	REQUIRED_FIELDS = ["username"]

	#REQUIRED_FIELDS = []

	objects = MyUserManager()

	class Meta:
		verbose_name = 'CustomUser'
		verbose_name_plural = 'CustomUsers'
		
	def get_full_name(self):
		return self.name
	
	def get_short_name(self):
		return self.name or self.email.split('@')[0]

	def __str__(self):
		return self.email
	



# class CustomUser(AbstractUser):
#     ROLES = (
#         ('admin', 'Admin'),
#         ('healthcare_provider', 'Healthcare Provider'),
#         ('patient', 'Patient'),
#     )
#     role = models.CharField(max_length=20, choices=ROLES)
#     groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
#     user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

# from django.contrib.auth.backends import BaseBackend
# from .models import CustomUser

# class CustomUserAuthBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = CustomUser.objects.get(username=username)
#             if user.check_password(password):
#                 return user
#         except CustomUser.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return CustomUser.objects.get(pk=user_id)
#         except CustomUser.DoesNotExist:
#             return None