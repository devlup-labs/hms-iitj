from django import forms
from .models import Prescription
from accounts.models import Appointment, Doctor


class TimeInput(forms.TimeInput):
    input_type = 'time'


class writePrescription(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['remarks']


class takeAppointmentForm(forms.ModelForm):

    specialization = forms.ChoiceField(choices=Doctor.SPECIALIZATION_CHOICES)

    class Meta:
        model = Appointment
        fields = ['time']
        widgets = {
            'time': TimeInput(),
        }
