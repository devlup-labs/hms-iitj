from django.db import models
from accounts.models import Patient


class Prescription(models.Model):
    TEST_CHOICES = (
        ('1', 'CBC'),
        ('2', 'Dengue'),
        ('3', 'Malaria'),
        ('4', 'Random Blood Sugar'),
        ('5', 'Pregnancy'),
        # ('1', 'Complete Blood Count'),
        # ('4', 'Liver Function Test'),
        # ('4', 'Renal Function Test'),
        # ('4', 'Lipid Profile'),
        # ('4', 'Urine Complete Examination'),
        # ('4', 'Stool Roitine '),
        # ('4', 'Rapid Test for Malaria'),
        # ('4', 'Dengue Serology'),
        # ('4', 'Blood Group and RH type'),
        # ('4', 'HBs Ag'),
        # ('4', 'HCV'),
        # ('4', 'HIV I & II'),
        # ('4', 'X Rays'),
    )
    prescription_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    remarks = models.TextField(max_length=240)


class Drug(models.Model):
    drug_id = models.CharField(unique=True, max_length=16)

    # DRUG LIST REQUIRED
    drug_name = models.CharField(max_length=40)


class PrescribedDrug(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.IntegerField()
