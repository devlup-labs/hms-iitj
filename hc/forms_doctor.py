from django import forms
from .models import Prescription
from main.models import Blog


class treatPatientForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['remarks']


class SearchPatientForm(forms.Form):

    email = forms.EmailField(max_length=100, label="Patient's Email")


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
