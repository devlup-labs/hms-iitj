from django.db import models
from accounts.models import Patient


class Prescription(models.Model):
    prescription_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    remarks = models.TextField(max_length=240)


class Drug(models.Model):
    drug_id = models.CharField(unique=True, max_length=16)
    drug_name = models.CharField(max_length=40)


class PrescribedDrug(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.IntegerField()
