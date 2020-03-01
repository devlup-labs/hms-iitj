from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
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
        ('1', 'Arthritis'),
        ('2', 'Asthma'),
        ('3', 'Cancer'),
        ('4', 'Kidney Disease'),
        ('5', 'Cystic Fibrosis'),
        ('6', 'Diabetes'),
        ('7', 'Heart Disease'),
        ('8', 'Osteoporosis'),
        ('8', 'Blood Pressure'),
        ('9', 'Others'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    phone_number = models.CharField(max_length=12)
    height = models.IntegerField(blank=False, null=False)
    weight = models.IntegerField(blank=False, null=False)
    blood_group = models.CharField(max_length=3, choices=BLOODGROUP_CHOICES)
    past_diseases = models.CharField(max_length=1, choices=DISEASE_CHOICES)
    other_diseases = models.CharField(max_length=20, null=True)
    allergies = models.CharField(max_length=20, null=True)
    emergency_contact = models.CharField(max_length=12)
    # prescription

    def __str__(self):
        return self.user.username
