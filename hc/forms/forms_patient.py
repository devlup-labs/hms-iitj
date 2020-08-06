from django import forms
from accounts.models import Patient, Doctor
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

    class DoctorChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.user.username + ", " + str(obj.specialization)

    doctor = DoctorChoiceField(queryset=Doctor.objects.all())
    time = forms.TimeField(widget=TimeInput())
    date = forms.DateField(widget=DateInput())

    def __init__(self, *args, **kwargs):
        super(takeAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['time'].initial = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%H:%M')
        self.fields['date'].initial = datetime.date.today


class AddFamilyMemberForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'gender', 'birthday', 'phone_number', 'emergency_phone',
            'height', 'weight', 'blood_group', 'past_diseases', 'other_diseases', 'allergies'
        ]
        widgets = {'birthday': forms.SelectDateWidget(years=YEARS)}

    def save(self, *args, **kwargs):
        self.instance.user = kwargs.pop('user', None)
        return super(AddFamilyMemberForm, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(AddFamilyMemberForm, self).__init__(*args, **kwargs)
        self.fields['height'].label = "Height (in cm) "
        self.fields['weight'].label = "Weight (in Kg) "

    def clean_phone_number(self):
        _dict = super(AddFamilyMemberForm, self).clean()
        if not _dict['phone_number'].isdigit() or len(_dict['phone_number']) < 10:
            raise forms.ValidationError('Phone number invalid')
        _dict['phone_number'] = _dict['phone_number'][-10:]
        return _dict['phone_number']

    def clean_emergency_phone(self):
        _dict = super(AddFamilyMemberForm, self).clean()
        if not _dict['emergency_phone'].isdigit() or len(_dict['emergency_phone']) < 10:
            raise forms.ValidationError('Phone number invalid')
        _dict['emergency_phone'] = _dict['emergency_phone'][-10:]
        return _dict['emergency_phone']
