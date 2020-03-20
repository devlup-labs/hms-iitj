from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Patient


class SignupFormforIIT(UserCreationForm):    # only for iitj students
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' ', 'icon': 'a'}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'maxlength': '254', 'placeholder': ' ', 'autocomplete': 'off'}))
    roll_no = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    password1 = forms.CharField(
        min_length=8, label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'placeholder': ' '}),)
    password2 = forms.CharField(
        label=("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),)
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES, required=True,
                               widget=forms.Select(attrs={'class': 'mdb-select'}))
    birthdate = forms.DateField(widget=forms.SelectDateWidget)
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'placeholder': ' '}), required=True)
    emergency_phone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'placeholder': ' '}), required=True)
    # height = forms.IntegerField(blank=False, null=False)
    height = forms.IntegerField(required=False)
    # weight = forms.IntegerField(blank=False, null=False)
    weight = forms.IntegerField(required=False)
    bloodgroup = forms.ChoiceField(choices=Patient.BLOODGROUP_CHOICES, required=True,
                                   widget=forms.Select(attrs={'class': 'mdb-select'}))
    past_diseases = forms.ChoiceField(choices=Patient.DISEASE_CHOICES,
                                      widget=forms.Select(attrs={'class': 'mdb-select'}), required=True)
    other_diseases = forms.CharField(max_length=20, required=False)
    allergies = forms.CharField(max_length=12, required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'roll_no', 'password1', 'password2', 'phone_number', 'gender']

    def clean_first_name(self):
        _dict = super(SignupFormforIIT, self).clean()
        return _dict['first_name'].capitalize()

    def clean_last_name(self):
        _dict = super(SignupFormforIIT, self).clean()
        return _dict['last_name'].capitalize()

    def clean_phone(self):
        _dict = super(SignupFormforIIT, self).clean()
        if not _dict['phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['phone'] = _dict['phone'][-10:]
        return _dict['phone']

    def clean_emergency_phone(self):
        _dict = super(SignupFormforIIT, self).clean()
        if not _dict['emergency_phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['emergency_phone'] = _dict['emergency_phone'][-10:]
        return _dict['emergency_phone']

    def clean_email(self):
        if User.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']

    def __init__(self, *args, **kwargs):
        super(SignupFormforIIT, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['icon_name'] = "fa fa-envelope"
        self.fields['username'].widget.attrs['icon_name'] = "fa fa-id-card"
        self.fields['first_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['last_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['password1'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['password2'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['phone_number'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['height'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['weight'].widget.attrs['icon_name'] = "fa fa-user"
