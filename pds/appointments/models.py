from django.db import models

# Create your models here.
from patients.models import Patient
from doctor.models import Doctor
from django.utils import timezone


class Appointment(models.Model):
    time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f"Appointment for {self.patient.name} with {self.doctor.name}"

