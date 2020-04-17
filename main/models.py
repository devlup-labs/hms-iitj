from django.db import models
from accounts.models import Doctor
from ckeditor_uploader.fields import RichTextUploadingField


class Blog(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    short_description = models.TextField()   # to be displayed on home page
    display_image = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        default='blog/default.png',
        help_text='This image will be displayed on the home page of website')
    content = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
