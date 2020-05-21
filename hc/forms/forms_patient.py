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
        exclude = ['user', 'prescriptions', 'staff']
        widgets = {'birthday': forms.SelectDateWidget(years=YEARS)}

    def __init__(self, *args, **kwargs):
        super(CreateProfileForm, self).__init__(*args, **kwargs)
        self.fields['num'].label = "Roll no. (or PF no.) "
        self.fields['height'].label = "Height (in cm) "
        self.fields['weight'].label = "Weight (in Kg) "

    def clean_phone_number(self):
        _dict = super(CreateProfileForm, self).clean()
        if not _dict['phone_number'].isdigit() or len(_dict['phone_number']) < 10:
            raise forms.ValidationError('Phone number invalid')
        _dict['phone_number'] = _dict['phone_number'][-10:]
        return _dict['phone_number']

    def clean_emergency_phone(self):
        _dict = super(CreateProfileForm, self).clean()
        if not _dict['emergency_phone'].isdigit() or len(_dict['emergency_phone']) < 10:
            raise forms.ValidationError('Phone number invalid')
        _dict['emergency_phone'] = _dict['emergency_phone'][-10:]
        return _dict['emergency_phone']


class takeAppointmentForm(forms.Form):

    specialization = forms.ModelChoiceField(queryset=DoctorSpecialization.objects.all(), initial=0)
    time = forms.TimeField(widget=TimeInput())
    date = forms.DateField(widget=DateInput())

    def __init__(self, *args, **kwargs):
        super(takeAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['time'].initial = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%H:%M')
        self.fields['date'].initial = datetime.date.today
