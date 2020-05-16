from django import forms
from hc.models import Prescription


class ViewPrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ViewPrescriptionForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['prescription_id'].widget.attrs['readonly'] = True
            self.fields['created_at'].widget.attrs['readonly'] = True
            self.fields['remarks'].widget.attrs['readonly'] = True
            self.fields['doctor'].widget.attrs['readonly'] = True
