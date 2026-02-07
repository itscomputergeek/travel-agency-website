from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator

class PackageCategory(models.Model):
    """Categories for travel packages (e.g., Adventure, Honeymoon, Family, Religious)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Package Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Package(models.Model):
    """Main travel package model"""
    # Basic Information
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(PackageCategory, on_delete=models.SET_NULL, null=True, related_name='packages')
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Brief description for package cards")

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         help_text="Original price before discount")
    currency = models.CharField(max_length=3, default='INR')

    # Trip Details
    duration_days = models.PositiveIntegerField(help_text="Number of days")
    duration_nights = models.PositiveIntegerField(help_text="Number of nights")
    location = models.CharField(max_length=200)
    destination_city = models.CharField(max_length=100)
    destination_state = models.CharField(max_length=100, blank=True)
    destination_country = models.CharField(max_length=100, default='India')

    # Images
    featured_image = models.ImageField(upload_to='packages/featured/')
    image_2 = models.ImageField(upload_to='packages/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='packages/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='packages/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='packages/', blank=True, null=True)

    # Inclusions & Exclusions
    inclusions = models.TextField(help_text="What's included (one per line)")
    exclusions = models.TextField(help_text="What's not included (one per line)")

    # Itinerary
    itinerary = models.TextField(help_text="Day-wise itinerary")

    # Additional Details
    highlights = models.TextField(help_text="Package highlights (one per line)", blank=True)
    activities = models.TextField(help_text="Activities included (one per line)", blank=True)
    hotel_type = models.CharField(max_length=100, blank=True, help_text="e.g., 3-star, 4-star, Resort")
    meal_plan = models.CharField(max_length=100, blank=True, help_text="e.g., Breakfast, All Meals")
    transport_mode = models.CharField(max_length=100, blank=True, help_text="e.g., Flight, Train, Bus")

    # Availability
    available = models.BooleanField(default=True)
    max_people = models.PositiveIntegerField(default=10)
    min_people = models.PositiveIntegerField(default=1)

    # SEO & Admin
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    popular = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_discount_percentage(self):
        """Calculate discount percentage if original price exists"""
        if self.original_price and self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return round(discount)
        return 0

    def get_price_per_day(self):
        """Calculate price per day"""
        if self.duration_days > 0:
            return round(self.price / self.duration_days, 2)
        return self.price

    def get_inclusions_list(self):
        """Return inclusions as a list"""
        return [item.strip() for item in self.inclusions.split('\n') if item.strip()]

    def get_exclusions_list(self):
        """Return exclusions as a list"""
        return [item.strip() for item in self.exclusions.split('\n') if item.strip()]

    def get_highlights_list(self):
        """Return highlights as a list"""
        return [item.strip() for item in self.highlights.split('\n') if item.strip()]


class PackageImage(models.Model):
    """Additional images for packages"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='packages/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.package.name} - Image {self.order}"


class PackageReview(models.Model):
    """Customer reviews for packages"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                        help_text="Rating out of 5")
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.package.name}"