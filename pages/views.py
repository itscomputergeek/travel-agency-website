from django.shortcuts import render, get_object_or_404
from packages.models import Package, PackageCategory
from testimonials.models import Testimonial
from .models import Page, SiteSettings, Slider


def home(request):
    """Homepage view"""
    # Get featured packages
    featured_packages = Package.objects.filter(featured=True, available=True)[:8]

    # Get popular packages
    popular_packages = Package.objects.filter(popular=True, available=True)[:8]

    # Get featured testimonials
    testimonials = Testimonial.objects.filter(approved=True, featured=True)[:6]

    # Get categories
    categories = PackageCategory.objects.all()[:6]

    # Get sliders
    sliders = Slider.objects.filter(active=True)

    # Get site settings
    try:
        site_settings = SiteSettings.objects.first()
    except:
        site_settings = None

    context = {
        'featured_packages': featured_packages,
        'popular_packages': popular_packages,
        'testimonials': testimonials,
        'categories': categories,
        'sliders': sliders,
        'site_settings': site_settings,
    }
    return render(request, 'home/index.html', context)


def about(request):
    """About us page"""
    try:
        site_settings = SiteSettings.objects.first()
    except:
        site_settings = None

    context = {
        'site_settings': site_settings,
    }
    return render(request, 'pages/about.html', context)


def contact(request):
    """Contact page"""
    try:
        site_settings = SiteSettings.objects.first()
    except:
        site_settings = None

    context = {
        'site_settings': site_settings,
    }
    return render(request, 'pages/contact.html', context)


def page_detail(request, slug):
    """Dynamic page view"""
    page = get_object_or_404(Page, slug=slug, active=True)
    context = {
        'page': page,
    }
    return render(request, 'pages/page_detail.html', context)
