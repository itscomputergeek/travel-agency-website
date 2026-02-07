from django.db import models
from django.utils.text import slugify

class Page(models.Model):
    """Static pages like About Us, Terms & Conditions, Privacy Policy"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Website settings and configuration"""
    site_name = models.CharField(max_length=200, default='Travel Agency')
    site_tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)

    # Contact Information
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    contact_phone_2 = models.CharField(max_length=15, blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    address = models.TextField()

    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # Homepage Content
    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.CharField(max_length=200, blank=True)
    hero_image = models.ImageField(upload_to='site/hero/', blank=True, null=True)

    about_us_short = models.TextField(blank=True, help_text="Short about us for homepage")

    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name


class Slider(models.Model):
    """Homepage slider/carousel"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='slider/')
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
