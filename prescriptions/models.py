from django.db import models

# Create your models here.
from patients.models import Patient
from doctor.models import Doctor

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateField()

    def __str__(self):
        return f"{self.patient.name} - {self.medication_name}"
