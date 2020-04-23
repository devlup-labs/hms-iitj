from django import forms
from accounts.models import Patient, Doctor
import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class CreateProfileIITForm(forms.ModelForm):    # only for iitj students

    class Meta:
        model = Patient
        exclude = ['user', 'prescriptions']
        widgets = {'birthday': DateInput}

    def __init__(self, *args, **kwargs):
        super(CreateProfileIITForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['height'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['weight'].widget.attrs['icon_name'] = "fa fa-user"


class takeAppointmentForm(forms.Form):

    specialization = forms.ChoiceField(choices=Doctor.SPECIALIZATION_CHOICES)
    time = forms.TimeField(widget=TimeInput(), initial=(
        datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%H:%M'))
    date = forms.DateField(widget=DateInput(), initial=datetime.date.today)
