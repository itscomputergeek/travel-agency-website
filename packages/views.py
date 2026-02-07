from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Package, PackageCategory


def package_list(request):
    """Display all packages with filtering and pagination"""
    packages = Package.objects.filter(available=True)

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        packages = packages.filter(category__slug=category_slug)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        packages = packages.filter(
            Q(name__icontains=search_query) |
            Q(destination_city__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        packages = packages.filter(price__gte=min_price)
    if max_price:
        packages = packages.filter(price__lte=max_price)

    # Sorting
    sort_by = request.GET.get('sort', '-featured')
    if sort_by in ['price', '-price', 'duration_days', '-duration_days', '-created_at']:
        packages = packages.order_by(sort_by)

    # Pagination
    paginator = Paginator(packages, 12)  # 12 packages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = PackageCategory.objects.all()

    context = {
        'packages': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
    }
    return render(request, 'packages/package_list.html', context)


def package_detail(request, slug):
    """Display package details"""
    package = get_object_or_404(Package, slug=slug, available=True)

    # Increment views
    package.views += 1
    package.save(update_fields=['views'])

    # Get related packages (same category)
    related_packages = Package.objects.filter(
        category=package.category,
        available=True
    ).exclude(id=package.id)[:4]

    # Get approved reviews
    reviews = package.reviews.filter(approved=True)

    context = {
        'package': package,
        'related_packages': related_packages,
        'reviews': reviews,
        'gallery_images': package.gallery_images.all(),
    }
    return render(request, 'packages/package_detail.html', context)
