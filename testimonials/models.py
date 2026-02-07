from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Testimonial(models.Model):
    """Customer testimonials and reviews"""

    # Customer Information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True)
    customer_location = models.CharField(max_length=100, blank=True, help_text="City or Country")
    customer_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    # Trip Information
    package_name = models.CharField(max_length=200, help_text="Which package they booked")
    trip_date = models.DateField(blank=True, null=True)

    # Review Content
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating out of 5"
    )
    title = models.CharField(max_length=200, help_text="Short headline for the review")
    review = models.TextField(help_text="Detailed review")

    # Trip Photos
    photo_1 = models.ImageField(upload_to='testimonials/photos/', blank=True, null=True)
    photo_2 = models.ImageField(upload_to='testimonials/photos/', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='testimonials/photos/', blank=True, null=True)

    # Status & Display
    approved = models.BooleanField(default=False, help_text="Show on website")
    featured = models.BooleanField(default=False, help_text="Display on homepage")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.customer_name} - {self.package_name}"

    def get_star_rating(self):
        """Return star rating as string for display"""
        return '⭐' * self.rating
