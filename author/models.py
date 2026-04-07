from django.db import models
from django.utils.text import slugify

from core.models import BaseModel
from user.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Author(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author', null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    name_bn = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_bn = models.TextField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='author_profiles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self): 
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            while Author.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{Author.objects.filter(slug=self.slug).count() + 1}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

class AuthorTag(BaseModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=100, unique=True)
    name_bn = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author Tag"
        verbose_name_plural = "Author Tags"
