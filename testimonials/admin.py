from django.contrib import admin
from django.utils.html import format_html
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = [
        'customer_name',
        'package_name',
        'rating_display',
        'trip_date',
        'approved',
        'featured',
        'created_at'
    ]
    list_filter = ['approved', 'featured', 'rating', 'trip_date', 'created_at']
    search_fields = ['customer_name', 'package_name', 'title', 'review', 'customer_location']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Customer Information', {
            'fields': (
                'customer_name',
                'customer_email',
                'customer_location',
                'customer_photo'
            )
        }),
        ('Trip Details', {
            'fields': (
                'package_name',
                'trip_date'
            )
        }),
        ('Review Content', {
            'fields': (
                'rating',
                'title',
                'review'
            )
        }),
        ('Trip Photos', {
            'fields': (
                'photo_1',
                'photo_2',
                'photo_3'
            ),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': (
                'approved',
                'featured'
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )

    def rating_display(self, obj):
        stars = '⭐' * obj.rating
        return format_html('<span style="font-size: 18px;">{}</span>', stars)
    rating_display.short_description = 'Rating'

    actions = ['approve_testimonials', 'unapprove_testimonials', 'make_featured', 'remove_featured']

    def approve_testimonials(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f'{updated} testimonial(s) approved.')
    approve_testimonials.short_description = 'Approve selected testimonials'

    def unapprove_testimonials(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f'{updated} testimonial(s) unapproved.')
    unapprove_testimonials.short_description = 'Unapprove selected testimonials'

    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} testimonial(s) marked as featured.')
    make_featured.short_description = 'Mark as featured'

    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f'{updated} testimonial(s) removed from featured.')
    remove_featured.short_description = 'Remove from featured'
