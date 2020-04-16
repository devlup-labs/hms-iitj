from django.db import models
from django.contrib.auth.models import User
from hc.models import Prescription
# from django.db.models.signals import pre_save  # , post_save


class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
    )
    BLOODGROUP_CHOICES = (
        ('O+', 'O Positive'),
        ('O-', 'O Negative'),
        ('A+', 'A Positive'),
        ('A-', 'A Negative'),
        ('B+', 'B Positive'),
        ('B-', 'B Negative'),
        ('AB+', 'AB Positive'),
        ('AB-', 'AB Negative'),
        ('NA', 'Don\'t Know'),
    )
    DISEASE_CHOICES = (
        ('0', 'Nill'),
        ('1', 'Asthma'),
        ('2', 'Kidney Disease'),
        ('3', 'Tuberculosis'),
        ('4', 'Irritable Bowel Syndrome'),
        ('5', 'Psychiatric Diseases'),
        ('6', 'Blood Diseases'),
        ('7', 'Liver Diseases'),
        ('8', 'Diabetes'),
        ('9', 'Heart Disease'),
        ('10', 'Osteoporosis'),
        ('11', 'Hyper Tension'),
        ('12', 'Cancer'),
        ('13', 'Stroke and Ceribro Vascular diseases'),
        ('14', 'Alzhemiers'),
        ('15', 'Pnemonia and Influenza'),
        ('16', 'Arthritis'),
        ('17', 'Others'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    roll_no = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    birthday = models.DateField(auto_now=False)
    phone_number = models.CharField(max_length=12)
    emergency_phone = models.CharField(max_length=12)
    height = models.IntegerField()
    weight = models.IntegerField()
    blood_group = models.CharField(max_length=3, choices=BLOODGROUP_CHOICES, default='O+')
    past_diseases = models.CharField(max_length=2, choices=DISEASE_CHOICES, default='0')
    other_diseases = models.CharField(max_length=20, default="nil")
    allergies = models.CharField(max_length=20, null=True, default="nil")
    prescriptions = models.ManyToManyField(Prescription, related_name="history", blank=True)

    def __str__(self):
        return self.user.username


class PatientOutsider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=Patient.GENDER_CHOICES, default='M')
    phone_number = models.CharField(max_length=12)
    blood_group = models.CharField(max_length=3, choices=Patient.BLOODGROUP_CHOICES, default='O+')
    prescriptions = models.ManyToManyField(Prescription, related_name="outsiderHistory", blank=True)

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = (
        ('1', 'General Physician'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=Patient.GENDER_CHOICES)
    specialization = models.CharField(max_length=1, choices=SPECIALIZATION_CHOICES)
    # shift_begin = models.TimeField(auto_now=False, auto_now_add=False)
    # shift_end = models.TimeField(auto_now=False, auto_now_add=False)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username  # first_name + " " + self.user.last_name


class Pharmacist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
