from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_prescription_id


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
    prescription_id = models.CharField(unique=True, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(max_length=240)
    doctor = models.ForeignKey(to='accounts.Doctor', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.prescription_id


def pre_save_prescription(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.prescription_id = unique_prescription_id(instance)


pre_save.connect(pre_save_prescription, sender=Prescription)


class Drug(models.Model):
    drug_id = models.CharField(unique=True, max_length=16)

    # DRUG LIST REQUIRED
    drug_name = models.CharField(max_length=40)


class PrescribedDrug(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Appointment(models.Model):
    doctor = models.ForeignKey(to="accounts.Doctor", on_delete=models.CASCADE,
                               related_name="app_doctor", blank=True, null=True)
    patient = models.ForeignKey(to="accounts.Patient", on_delete=models.CASCADE,
                                related_name="app_patient", blank=True, null=True)
    time = models.TimeField()
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE,
                                     related_name="app_prescription", blank=True, null=True)

    def __str__(self):
        return self.doctor.user.first_name + ", " + self.patient.user.first_name
