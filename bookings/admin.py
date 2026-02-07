from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, ContactInquiry


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_id',
        'full_name',
        'package',
        'travel_date',
        'number_of_people',
        'price_display',
        'payment_status_display',
        'booking_status',
        'created_at'
    ]
    list_filter = ['booking_status', 'payment_status', 'travel_date', 'created_at']
    search_fields = ['booking_id', 'full_name', 'email', 'phone', 'package__name']
    readonly_fields = ['booking_id', 'created_at', 'updated_at', 'balance_amount', 'payment_percentage']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Booking Information', {
            'fields': (
                'booking_id',
                'package',
                'booking_status',
                'payment_status'
            )
        }),
        ('Customer Details', {
            'fields': (
                'full_name',
                'email',
                'phone',
                'alternate_phone',
                'address',
                'city',
                'state',
                'pincode'
            )
        }),
        ('Travel Details', {
            'fields': (
                'travel_date',
                'number_of_people',
                'number_of_adults',
                'number_of_children',
                'special_requests'
            )
        }),
        ('Payment Information', {
            'fields': (
                'total_price',
                'advance_paid',
                'balance_amount',
                'payment_percentage'
            )
        }),
        ('Admin Section', {
            'fields': (
                'admin_notes',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )

    def price_display(self, obj):
        return format_html(
            '<strong>₹{}</strong><br><small>Paid: ₹{} | Balance: ₹{}</small>',
            obj.total_price,
            obj.advance_paid,
            obj.balance_amount
        )
    price_display.short_description = 'Price Details'

    def payment_status_display(self, obj):
        colors = {
            'pending': 'red',
            'paid': 'green',
            'partial': 'orange',
            'refunded': 'gray'
        }
        color = colors.get(obj.payment_status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_payment_status_display()
        )
    payment_status_display.short_description = 'Payment'

    def payment_percentage(self, obj):
        percentage = obj.get_payment_percentage()
        return format_html(
            '<div style="background: #f0f0f0; border-radius: 10px; height: 20px; width: 200px;">'
            '<div style="background: green; height: 100%; width: {}%; border-radius: 10px; text-align: center; color: white; font-size: 12px; line-height: 20px;">'
            '{}%'
            '</div></div>',
            percentage,
            percentage
        )
    payment_percentage.short_description = 'Payment Progress'

    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']

    def mark_confirmed(self, request, queryset):
        updated = queryset.update(booking_status='confirmed')
        self.message_user(request, f'{updated} booking(s) marked as confirmed.')
    mark_confirmed.short_description = 'Mark as confirmed'

    def mark_completed(self, request, queryset):
        updated = queryset.update(booking_status='completed')
        self.message_user(request, f'{updated} booking(s) marked as completed.')
    mark_completed.short_description = 'Mark as completed'

    def mark_cancelled(self, request, queryset):
        updated = queryset.update(booking_status='cancelled')
        self.message_user(request, f'{updated} booking(s) marked as cancelled.')
    mark_cancelled.short_description = 'Mark as cancelled'


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'phone',
        'inquiry_type',
        'status_display',
        'created_at'
    ]
    list_filter = ['inquiry_type', 'status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Inquiry Details', {
            'fields': (
                'name',
                'email',
                'phone',
                'inquiry_type',
                'subject',
                'message',
                'package'
            )
        }),
        ('Response', {
            'fields': (
                'status',
                'admin_response'
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

    def status_display(self, obj):
        colors = {
            'new': 'blue',
            'in_progress': 'orange',
            'resolved': 'green',
            'closed': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'

    actions = ['mark_in_progress', 'mark_resolved', 'mark_closed']

    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} inquiry(ies) marked as in progress.')
    mark_in_progress.short_description = 'Mark as in progress'

    def mark_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} inquiry(ies) marked as resolved.')
    mark_resolved.short_description = 'Mark as resolved'

    def mark_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} inquiry(ies) marked as closed.')
    mark_closed.short_description = 'Mark as closed'
