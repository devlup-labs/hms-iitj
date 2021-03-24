from django import forms
from .forms_patient import TimeInput
from hc.models import Appointment
from accounts.models import Doctor


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


class Doctor_Select(forms.Form):

    class DoctorChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.user.username + ", " + str(obj.specialization)

    doctor = DoctorChoiceField(queryset=Doctor.objects.all())
