from django import forms
from .models import Prescription


class writePrescription(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['remarks']
