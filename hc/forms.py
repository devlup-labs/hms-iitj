from django import forms
from .models import Prescription
from accounts.models import Doctor
import datetime


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


class treatPatientForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['remarks']


class takeAppointmentForm(forms.Form):

    specialization = forms.ChoiceField(choices=Doctor.SPECIALIZATION_CHOICES)
    time = forms.TimeField(widget=TimeInput(), initial=(
        datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%H:%M'))
    date = forms.DateField(widget=DateInput(), initial=datetime.date.today)


class SearchPatientForm(forms.Form):

    email = forms.EmailField(max_length=100, label="Patient's Email")
