from django.db import models
from core.models import BaseModel
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

class Blog(BaseModel):
    slug = models.SlugField(unique=True, null=True, blank=True)
    author_name = models.CharField(max_length=255, null=True)
    author_name_bn = models.CharField(max_length=255, null=True, blank=True)
    author_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    title = models.CharField(max_length=255, null=True)
    title_bn = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    subtitle_bn = models.CharField(max_length=255, null=True, blank=True)
    content = CKEditor5Field(null=True)
    content_bn = CKEditor5Field(null=True)
    cover_image = models.ImageField(upload_to='blog_images/', null=True)
    read_time = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    published_date = models.DateTimeField(null=True)
    is_featured = models.BooleanField(default=False)
    index_number = models.IntegerField(default=0, help_text="Order of the blog post")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.index_number:
            self.index_number = Blog.objects.count() + 1
            
        if not self.slug:
            while True:
                slug = slugify(self.title)
                if not Blog.objects.filter(slug=slug).exists():
                    self.slug = slug[:45]
                    break
            
        return super().save(*args, **kwargs)
