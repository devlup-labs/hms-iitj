from django import forms
from .forms_patient import TimeInput
from .models import Appointment


class ViewAppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'date': forms.SelectDateWidget(
                 empty_label=("Choose Year", "Choose Month", "Choose Day"),
            ),
            'time': TimeInput(),
        }
