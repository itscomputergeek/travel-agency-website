from django.contrib import admin
from .models import Page, SiteSettings, Slider


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'active', 'created_at', 'updated_at']
    list_filter = ['active', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'contact_phone', 'updated_at']
    readonly_fields = ['updated_at']

    fieldsets = (
        ('Site Information', {
            'fields': (
                'site_name',
                'site_tagline',
                'logo',
                'favicon'
            )
        }),
        ('Contact Information', {
            'fields': (
                'contact_email',
                'contact_phone',
                'contact_phone_2',
                'whatsapp_number',
                'address'
            )
        }),
        ('Social Media Links', {
            'fields': (
                'facebook_url',
                'instagram_url',
                'twitter_url',
                'youtube_url',
                'linkedin_url'
            ),
            'classes': ('collapse',)
        }),
        ('Homepage Content', {
            'fields': (
                'hero_title',
                'hero_subtitle',
                'hero_image',
                'about_us_short'
            )
        }),
        ('SEO Settings', {
            'fields': (
                'meta_description',
                'meta_keywords'
            ),
            'classes': ('collapse',)
        }),
        ('Last Updated', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        })
    )

    def has_add_permission(self, request):
        # Only allow one settings object
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'active', 'image_preview']
    list_filter = ['active']
    search_fields = ['title', 'subtitle']
    list_editable = ['order', 'active']

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" width="150" height="80" style="object-fit: cover;" />', obj.image.url)
        return 'No image'
    image_preview.short_description = 'Preview'
