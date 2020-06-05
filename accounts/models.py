from django.db import models
from django.contrib.auth.models import User
from hc.models import Prescription, DoctorSpecialization
from django.db.models.signals import post_save
from django.contrib.auth.models import Group


class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
    )
    BLOODGROUP_CHOICES = (
        ('NA', 'Don\'t Know'),
        ('O+', 'O Positive'),
        ('O-', 'O Negative'),
        ('A+', 'A Positive'),
        ('A-', 'A Negative'),
        ('B+', 'B Positive'),
        ('B-', 'B Negative'),
        ('AB+', 'AB Positive'),
        ('AB-', 'AB Negative'),
    )
    DISEASE_CHOICES = (
        ('1', 'Alzheimer’s'),
        ('2', 'Arthritis'),
        ('3', 'Asthma'),
        ('4', 'Blood Diseases'),
        ('5', 'Cancer'),
        ('6', 'Diabetes'),
        ('7', 'Heart Disease'),
        ('8', 'Hyper Tension'),
        ('9', 'Kidney Disease'),
        ('10', 'Liver Diseases'),
        ('11', 'Osteoporosis'),
        ('12', 'Pneumonia and Influenza'),
        ('13', 'Psychiatric Diseases'),
        ('14', 'Stroke and Cerebrovascular diseases'),
        ('15', 'Tuberculosis'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    num = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    birthday = models.DateField(auto_now=False)
    phone_number = models.CharField(max_length=12)
    emergency_phone = models.CharField(max_length=12)
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=3, choices=BLOODGROUP_CHOICES, default='NA')
    past_diseases = models.CharField(max_length=2, choices=DISEASE_CHOICES, null=True, blank=True)
    other_diseases = models.CharField(max_length=20, default="nil")
    allergies = models.CharField(max_length=20, null=True, default="nil")
    prescriptions = models.ManyToManyField(Prescription, related_name="history", blank=True)
    staff = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def post_save_user(sender, instance, created, **kwargs):
    if created:
        instance.username = instance.email.split('@')[0]
        group = Group.objects.get(name="patient")
        instance.groups.add(group)
        instance.save()


post_save.connect(post_save_user, sender=User)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=Patient.GENDER_CHOICES)
    specialization = models.ForeignKey(DoctorSpecialization, related_name="specializations",
                                       on_delete=models.SET_NULL, null=True)
    # shift_begin = models.TimeField(auto_now=False, auto_now_add=False)
    # shift_end = models.TimeField(auto_now=False, auto_now_add=False)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Pharmacist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
