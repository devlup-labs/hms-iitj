from django.db import models
from accounts.models import Doctor
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation


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
    published_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            if Blog.objects.filter(title=(self.title)).exists():
                count = Blog.objects.filter(title=(self.title)).count()
                self.slug = "%s-%s" % (slugify(kwargs.pop('title', self.title)), count+1)
            else:
                self.slug = slugify(kwargs.pop('title', self.title))
        return super(Blog, self).save(*args, **kwargs)
