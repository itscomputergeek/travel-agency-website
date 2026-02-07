from django.db import models
from django.core.validators import MinValueValidator, EmailValidator
from packages.models import Package

class Booking(models.Model):
    """Customer bookings for travel packages"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('refunded', 'Refunded'),
    ]

    # Package & Customer Info
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='bookings')

    # Customer Details
    full_name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # Booking Details
    number_of_people = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    number_of_adults = models.PositiveIntegerField(default=1)
    number_of_children = models.PositiveIntegerField(default=0)
    travel_date = models.DateField()
    special_requests = models.TextField(blank=True, help_text="Any special requirements or requests")

    # Pricing
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Status
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')

    # Admin Notes
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin use")

    # Timestamps
    booking_id = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def save(self, *args, **kwargs):
        if not self.booking_id:
            # Generate booking ID: BKG + timestamp
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.booking_id = f'BKG{timestamp}'

        # Calculate balance amount
        self.balance_amount = self.total_price - self.advance_paid

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.full_name} - {self.package.name}"

    def get_payment_percentage(self):
        """Calculate percentage of payment made"""
        if self.total_price > 0:
            return round((self.advance_paid / self.total_price) * 100, 2)
        return 0


class ContactInquiry(models.Model):
    """Contact form inquiries"""

    INQUIRY_TYPE = [
        ('general', 'General Inquiry'),
        ('package', 'Package Inquiry'),
        ('booking', 'Booking Related'),
        ('complaint', 'Complaint'),
        ('feedback', 'Feedback'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    # Contact Information
    name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE, default='general')
    message = models.TextField()

    # Optional package reference
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='inquiries')

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_response = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} - {self.subject}"
