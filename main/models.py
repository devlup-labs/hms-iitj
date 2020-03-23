from django.db import models
from accounts.models import Doctor
from ckeditor_uploader.fields import RichTextUploadingField


class blog(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    short_description = models.TextField()   # to be displayed on home page
    content = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(auto_now_add=True)
