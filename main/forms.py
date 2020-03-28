from django import forms
from .models import blog


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = blog
        fields = '__all__'
