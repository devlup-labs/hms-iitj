from django import forms
from accounts.models import Patient, DoctorSpecialization
import datetime


YEARS = [-x for x in range(-datetime.date.today().year, -1930)]


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateProfileForm(forms.ModelForm):    # only for iitj students

    class Meta:
        model = Patient
        exclude = ['user', 'prescriptions']
        widgets = {'birthday': forms.SelectDateWidget(years=YEARS)}

    def __init__(self, *args, **kwargs):
        super(CreateProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['height'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['weight'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['num'].label = "Roll no. (or PF no.) "


class takeAppointmentForm(forms.Form):

    specialization = forms.ModelChoiceField(queryset=DoctorSpecialization.objects.all(), initial=0)
    time = forms.TimeField(widget=TimeInput(), initial=(
        datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%H:%M'))
    date = forms.DateField(widget=DateInput(), initial=datetime.date.today)
