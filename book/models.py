import uuid
from django.db import models
from core.models import BaseModel
from order.models import OrderItem, Order
from user.models import User
from django.utils.text import slugify
from author.models import Author
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field

class Book(BaseModel):
    
    STATUS = (
        ('published', 'Published'), 
        ('draft', 'Draft'),
        ('archived', 'Archived')
    )
    
    title = models.CharField(max_length=255)
    title_bn = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name='books', null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    sku = models.CharField(max_length=100, null=True, blank=True, help_text="Stock Keeping Unit")
    description = CKEditor5Field(blank=True, null=True)
    description_bn = CKEditor5Field(blank=True, null=True)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, null=True, blank=True, help_text="International Standard Book Number")
    pages = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available_copies = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, help_text="Average rating of the book")
    rating_count = models.PositiveIntegerField(default=0, help_text="Total number of ratings given to the book")
    categories = models.ManyToManyField('Category', related_name='books', blank=True)
    tags = models.ManyToManyField('Tag', related_name='books', blank=True)
    publisher_name = models.CharField(max_length=255, blank=True, null=True)
    publisher_website_link = models.URLField(blank=True, null=True)
    translator = models.CharField(max_length=255, blank=True, null=True)
    edition = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    dimensions = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., '5 x 8 inches'")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="in grams")
    country = models.CharField(max_length=100, blank=True, null=True, help_text="Country of publication")
    is_new_arrival = models.BooleanField(default=False, help_text="If true, the book will be shown on the new arrival section")
    is_popular = models.BooleanField(default=False, help_text="If true, the book will be shown on the favorite section")
    is_comming_soon = models.BooleanField(default=False, help_text="If true, the book will be shown on the comming soon section")
    is_best_seller = models.BooleanField(default=False, help_text="If true, the book will be shown on the best seller section")
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-published_date']
        
    def get_book_price(self):
        if self.discounted_price and self.discounted_price > 0:
            return self.discounted_price
        return self.price
    
    def user_can_give_review(self, user):
        if not user.is_authenticated:
            return False
        return not self.reviews.filter(is_active=True, user=user).exists()        

# Book Preview Images that will be shown on the book detail page for reading book.
class BookPreview(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='previews')
    image = models.ImageField(upload_to='book_previews/', blank=True, null=True)
    index_number = models.PositiveIntegerField(default=0) # for sorting
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Book Preview"
        verbose_name_plural = "Book Previews"
        ordering = ['index_number']

    def save(self, *args, **kwargs):
        if not self.index_number:
            self.index_number = BookPreview.objects.filter(book=self.book).count() + 1
        super().save(*args, **kwargs)


class BookImage(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='book_images/', null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    index_number = models.PositiveIntegerField(default=0) # for sorting
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Book Image"
        verbose_name_plural = "Book Images"
        ordering = ['index_number']

    def __str__(self):
        return f"Image for {self.book.title}"
    
    def save(self, *args, **kwargs):
        if not self.index_number:
            self.index_number = BookImage.objects.filter(book=self.book).count() + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Book Image"
        verbose_name_plural = "Book Images"
        ordering = ['book__title']  # Order by book title


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    name_bn = models.CharField(max_length=100, blank=True, null=True, help_text="Bengali name of the category")
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    index_number = models.PositiveIntegerField(default=0) # for sorting
    is_featured = models.BooleanField(default=False, help_text="Featured category will be shown on the home page")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['index_number']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            while True:
                slug = slugify(self.name)
                if not Category.objects.filter(slug=slug).exists():
                    self.slug = slug
                    break
                self.name = f"{self.name} {Category.objects.filter(slug=slug).count() + 1}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
class Tag(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class SpecialPackage(BaseModel):
    uuid = models.UUIDField(editable=False, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    name_bn = models.CharField(max_length=100, blank=True, null=True, help_text="Bengali name of the special package")
    description = models.TextField(blank=True, null=True)
    description_bn = models.TextField(blank=True, null=True, help_text="Bengali description of the special package")
    image = models.ImageField(upload_to='special_package_images/', blank=True, null=True)
    index_number = models.PositiveIntegerField(default=0) # for sorting
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Featured special package will be shown on the home page")
    books = models.ManyToManyField(Book, blank=True, through='SpecialPackageBook', related_name='special_packages')

    class Meta:
        verbose_name = "Special Package"
        
    def save(self, *args, **kwargs):
        while True:
            if not self.uuid:
                self.uuid = uuid.uuid4()
            if not SpecialPackage.objects.filter(uuid=self.uuid).exists():
                break
            self.uuid = uuid.uuid4()
        super().save()


class SpecialPackageBook(BaseModel):
    package = models.ForeignKey(SpecialPackage, on_delete=models.CASCADE, related_name='package_books', null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books', null=True)
    index_number = models.PositiveIntegerField(default=0) # for sorting
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Special Package Book"
        verbose_name_plural = "Special Package Books"


class BookReview(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Book Review"
        verbose_name_plural = "Book Reviews"
        ordering = ['-created_at']

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5")
        
        if BookReview.objects.filter(book=self.book, user=self.user).exists():
            raise ValidationError("You have already reviewed this book")