from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Carousel(BaseModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    title_bn = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    subtitle_bn = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='carousel_images/')
    link = models.URLField(blank=True, null=True)
    index_number = models.PositiveIntegerField(default=0, help_text="Order of the carousel item")
    is_active = models.BooleanField(default=True, help_text="Is the carousel item currently active?")
    # This field is used to mark carousel items as advertisements
    # Only up to 2 items can be marked as advertisements
    # is_advertise = models.BooleanField(default=False)

    class Meta:
        ordering = ['index_number']

    def __str__(self):
        return self.title if self.title else "Carousel Image"

    class Meta:
        verbose_name = "Carousel"
        verbose_name_plural = "Carousels"
        ordering = ['-created_at']  # Order by creation date descending
        
    # def clean(self):
    #     if Carousel.objects.filter(is_advertise=True).count() > 2 and self.is_advertise:
    #         raise ValueError("Only up to 2 carousel items can be marked as advertisements.")
    #     return super().clean()
    

class GeneralData(BaseModel):
    
    # Website Information
    website_logo = models.ImageField(upload_to='website_logos/', blank=True, null=True)

    # Social Media Links
    address = models.CharField(max_length=255, blank=True, null=True)
    address_bn = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    # Articles
    articles_section_title = models.CharField(max_length=255, blank=True, null=True)
    articles_section_title_bn = models.CharField(max_length=255, blank=True, null=True)
    articles_section_subtitle = models.CharField(max_length=255, blank=True, null=True)
    articles_section_subtitle_bn = models.CharField(max_length=255, blank=True, null=True)

    # Delivery Charge
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

    def __str__(self):
        return self.address if self.address else "General Data"


class Support(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Support"
        verbose_name_plural = "Supports"
        ordering = ['-created_at']

class Country(BaseModel):
    name = models.CharField(max_length=255, null=True)
    name_bn = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255, null=True)
    flag = models.ImageField(upload_to='country_flags/', null=True, blank=True)

    def __str__(self):
        return str(self.name) if self.name else "Country"

    class Meta:
        verbose_name = "Country"


class State(BaseModel):
    name = models.CharField(max_length=255, null=True)
    name_bn = models.CharField(max_length=255, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states', null=True, blank=True)

    def __str__(self):
        return str(self.name) if self.name else "State"

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"

class City(BaseModel):
    name = models.CharField(max_length=255, null=True)
    name_bn = models.CharField(max_length=255, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities', null=True)

    def __str__(self):
        return str(self.name) if self.name else "City"

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

class Thana(BaseModel):
    name = models.CharField(max_length=255, null=True)
    name_bn = models.CharField(max_length=255, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='thanas', null=True)

    def __str__(self):
        return str(self.name) if self.name else "Thana"

    class Meta:
        verbose_name = "Thana"
        verbose_name_plural = "Thanas"

class Testimonial(BaseModel):
    name = models.CharField(max_length=255, null=True)
    name_bn = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    designation_bn = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    city_bn = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True)
    comment_bn = models.TextField(null=True)
    rating = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)

    def __str__(self):
        return self.name
