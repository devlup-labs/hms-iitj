from django import forms
from hc.models import Prescription


class treatPatientForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['remarks']


class SearchPatientForm(forms.Form):

    username = forms.CharField(max_length=50, label="Patient's Username")
