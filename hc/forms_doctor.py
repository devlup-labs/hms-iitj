from django import forms
from .models import Prescription


class treatPatientForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['remarks']


class SearchPatientForm(forms.Form):

    email = forms.EmailField(max_length=100, label="Patient's Email")
