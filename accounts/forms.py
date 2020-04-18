from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Patient


class DateInput(forms.DateInput):
    input_type = 'date'


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
