from django import forms
from main.models import Blog


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ['author']
