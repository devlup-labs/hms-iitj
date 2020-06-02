from django import forms
from hc.models import Prescription
from accounts.models import Patient


class treatPatientForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['remarks']


class SearchPatientForm(forms.Form):

    email = forms.EmailField(label="Email")
    username = forms.ChoiceField(label="Patient's Username")

    def __init__(self, *args, **kwargs):
        super(SearchPatientForm, self).__init__(*args, **kwargs)
        self.fields['username'].queryset = Patient.objects.none()
