from django import forms
from .models import Prescription
from accounts.models import Doctor

class writePrescription(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['remarks']


class takeAppointment(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization']
        