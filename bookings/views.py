from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from packages.models import Package
from .models import Booking, ContactInquiry


def booking_create(request, package_slug):
    """Create a new booking"""
    package = get_object_or_404(Package, slug=package_slug, available=True)

    if request.method == 'POST':
        # Get form data
        booking = Booking(
            package=package,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            alternate_phone=request.POST.get('alternate_phone', ''),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            number_of_people=request.POST.get('number_of_people'),
            number_of_adults=request.POST.get('number_of_adults', 1),
            number_of_children=request.POST.get('number_of_children', 0),
            travel_date=request.POST.get('travel_date'),
            special_requests=request.POST.get('special_requests', ''),
            total_price=float(request.POST.get('total_price')),
            advance_paid=float(request.POST.get('advance_paid', 0)),
        )
        booking.save()

        # Send confirmation email (optional)
        try:
            send_mail(
                f'Booking Confirmation - {booking.booking_id}',
                f'Dear {booking.full_name},\n\nYour booking for {package.name} has been received.\n\nBooking ID: {booking.booking_id}\n\nWe will contact you shortly.\n\nThank you!',
                settings.DEFAULT_FROM_EMAIL,
                [booking.email],
                fail_silently=True,
            )
        except:
            pass

        messages.success(request, f'Booking created successfully! Your booking ID is {booking.booking_id}')
        return redirect('booking_success', booking_id=booking.booking_id)

    context = {
        'package': package,
    }
    return render(request, 'bookings/booking_form.html', context)


def booking_success(request, booking_id):
    """Display booking confirmation"""
    booking = get_object_or_404(Booking, booking_id=booking_id)
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_success.html', context)


def contact_create(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        inquiry = ContactInquiry(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            subject=request.POST.get('subject'),
            inquiry_type=request.POST.get('inquiry_type', 'general'),
            message=request.POST.get('message'),
        )

        package_id = request.POST.get('package_id')
        if package_id:
            inquiry.package_id = package_id

        inquiry.save()

        messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        return redirect('contact')

    return render(request, 'pages/contact.html')
