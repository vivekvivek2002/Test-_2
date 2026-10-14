from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Show or hide this category on the public website.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True, help_text="Controls if this product is publicly visible.")
    is_featured = models.BooleanField(default=False, help_text="Feature this product on the homepage.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})


class Banner(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=50, default='Learn More')
    button_link = models.CharField(max_length=200, default='/')
    is_active = models.BooleanField(default=True, help_text="Display in the hero carousel on the homepage.")
    order = models.PositiveIntegerField(default=0, help_text="Display order in hero carousel (lower numbers first).")

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title
