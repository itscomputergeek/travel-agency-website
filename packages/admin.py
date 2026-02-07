from django.contrib import admin
from django.utils.html import format_html
from .models import PackageCategory, Package, PackageImage, PackageReview


class PackageImageInline(admin.TabularInline):
    """Inline admin for package gallery images"""
    model = PackageImage
    extra = 1
    fields = ['image', 'caption', 'order']


class PackageReviewInline(admin.TabularInline):
    """Inline admin for package reviews"""
    model = PackageReview
    extra = 0
    readonly_fields = ['name', 'email', 'rating', 'review', 'created_at']
    fields = ['name', 'rating', 'review', 'approved', 'created_at']
    can_delete = True


@admin.register(PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'package_count', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

    def package_count(self, obj):
        return obj.packages.count()
    package_count.short_description = 'Number of Packages'


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'price_display',
        'duration_display',
        'destination_city',
        'available',
        'featured',
        'views',
        'created_at'
    ]
    list_filter = ['category', 'available', 'featured', 'popular', 'destination_country', 'created_at']
    search_fields = ['name', 'destination_city', 'location', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['views', 'created_at', 'updated_at', 'discount_display', 'price_per_day_display']

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'slug',
                'category',
                'short_description',
                'description'
            )
        }),
        ('Pricing', {
            'fields': (
                'price',
                'original_price',
                'currency',
                'discount_display',
                'price_per_day_display'
            )
        }),
        ('Trip Details', {
            'fields': (
                'duration_days',
                'duration_nights',
                'location',
                'destination_city',
                'destination_state',
                'destination_country'
            )
        }),
        ('Images', {
            'fields': (
                'featured_image',
                'image_2',
                'image_3',
                'image_4',
                'image_5'
            ),
            'classes': ('collapse',)
        }),
        ('Inclusions & Exclusions', {
            'fields': (
                'inclusions',
                'exclusions'
            )
        }),
        ('Itinerary & Details', {
            'fields': (
                'itinerary',
                'highlights',
                'activities',
                'hotel_type',
                'meal_plan',
                'transport_mode'
            ),
            'classes': ('collapse',)
        }),
        ('Availability Settings', {
            'fields': (
                'available',
                'max_people',
                'min_people'
            )
        }),
        ('Display Options', {
            'fields': (
                'featured',
                'popular',
                'views'
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

    inlines = [PackageImageInline, PackageReviewInline]

    def price_display(self, obj):
        discount = obj.get_discount_percentage()
        if discount > 0:
            return format_html(
                '<strong style="color: green;">₹{}</strong> <del style="color: red;">₹{}</del> <span style="color: orange;">({}% off)</span>',
                obj.price,
                obj.original_price,
                discount
            )
        return f'₹{obj.price}'
    price_display.short_description = 'Price'

    def duration_display(self, obj):
        return f'{obj.duration_days}D/{obj.duration_nights}N'
    duration_display.short_description = 'Duration'

    def discount_display(self, obj):
        discount = obj.get_discount_percentage()
        if discount > 0:
            return format_html(
                '<strong style="color: green; font-size: 16px;">{}% OFF</strong>',
                discount
            )
        return 'No discount'
    discount_display.short_description = 'Current Discount'

    def price_per_day_display(self, obj):
        return f'₹{obj.get_price_per_day()} per day'
    price_per_day_display.short_description = 'Price Per Day'

    actions = ['make_featured', 'remove_featured', 'make_available', 'make_unavailable']

    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} package(s) marked as featured.')
    make_featured.short_description = 'Mark selected packages as featured'

    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f'{updated} package(s) removed from featured.')
    remove_featured.short_description = 'Remove from featured'

    def make_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f'{updated} package(s) marked as available.')
    make_available.short_description = 'Mark as available'

    def make_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f'{updated} package(s) marked as unavailable.')
    make_unavailable.short_description = 'Mark as unavailable'


@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ['package', 'caption', 'order', 'image_preview']
    list_filter = ['package']
    search_fields = ['package__name', 'caption']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return 'No image'
    image_preview.short_description = 'Preview'


@admin.register(PackageReview)
class PackageReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'package', 'rating_display', 'approved', 'created_at']
    list_filter = ['approved', 'rating', 'created_at']
    search_fields = ['name', 'email', 'package__name', 'review']
    readonly_fields = ['created_at']

    actions = ['approve_reviews', 'unapprove_reviews']

    def rating_display(self, obj):
        stars = '⭐' * obj.rating
        return format_html('<span style="font-size: 18px;">{}</span>', stars)
    rating_display.short_description = 'Rating'

    def approve_reviews(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f'{updated} review(s) approved.')
    approve_reviews.short_description = 'Approve selected reviews'

    def unapprove_reviews(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f'{updated} review(s) unapproved.')
    unapprove_reviews.short_description = 'Unapprove selected reviews'
