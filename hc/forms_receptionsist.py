from django import forms
from .models import Appointment


class ViewAppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = '__all__'
