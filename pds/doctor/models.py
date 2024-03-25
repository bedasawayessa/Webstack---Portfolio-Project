from django.db import models
from users.models import CustomUser

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    
    def __str__(self):
        return self.name
