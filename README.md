# Travel Agency Website

A fully functional travel agency website built with Django and Python, featuring package management, booking system, testimonials, and a powerful admin panel.

## Features

### User Features
- **Homepage**: Beautiful landing page with featured packages, search functionality, and testimonials
- **Package Browsing**: Filter and search travel packages by category, price, destination
- **Package Details**: Detailed package information with images, itinerary, inclusions/exclusions
- **Booking System**: Complete booking form with customer details and payment tracking
- **Contact Form**: Easy-to-use contact form for inquiries
- **Responsive Design**: Mobile-friendly layout that works on all devices

### Admin Features
- **Easy Package Management**: Add, edit, delete packages with rich admin interface
- **Price & Discount Management**: Set original prices and discounts
- **Image Management**: Upload multiple images for each package
- **Booking Management**: View and manage all bookings with status tracking
- **Payment Tracking**: Monitor advance payments and balance amounts
- **Testimonial Management**: Approve and feature customer testimonials
- **Contact Inquiry Management**: Respond to customer inquiries
- **Site Settings**: Manage site-wide settings, contact information, social media links

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Navigate to Project Directory**
   ```bash
   cd c:\Users\Administrator\travel_agency
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Superuser (Admin Account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin username, email, and password.

4. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access the Website**
   - **Frontend**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/

## Admin Panel Guide

### Access Admin Panel
1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials

### Adding Your First Package

1. **Create Package Category** (Optional)
   - Go to "Package Categories" → "Add Package Category"
   - Enter category name (e.g., "Adventure", "Honeymoon", "Religious")
   - Save

2. **Add a New Package**
   - Go to "Packages" → "Add Package"
   - Fill in the required fields:
     - Name, Category, Description
     - Price (you can add original price for discount display)
     - Duration (days and nights)
     - Location and destination details
     - Upload featured image
     - Add inclusions and exclusions (one per line)
     - Add itinerary
   - Mark as "Featured" to show on homepage
   - Save

3. **Configure Site Settings**
   - Go to "Site Settings"
   - Add your contact information, social media links
   - Set homepage hero text
   - Save

### Managing Bookings
- View all bookings in the "Bookings" section
- Update booking status (Pending → Confirmed → Completed)
- Track payment status
- Add admin notes for internal reference

### Managing Testimonials
- Approve customer testimonials
- Mark testimonials as "Featured" to show on homepage
- Edit customer details and review content

## Project Structure

```
travel_agency/
├── packages/          # Package management app
├── bookings/          # Booking and inquiry management
├── testimonials/      # Customer testimonials
├── pages/            # Static pages and site settings
├── users/            # User management (for future use)
├── templates/        # HTML templates
│   ├── base.html    # Base template with navigation & footer
│   ├── home/        # Homepage templates
│   ├── packages/    # Package listing and detail templates
│   ├── bookings/    # Booking form templates
│   └── pages/       # Contact, About, and other pages
├── static/          # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/           # User uploaded files (package images, etc.)
└── travel_agency/   # Project settings
```

## Key Features in Admin Panel

### Package Admin
- ✅ Visual price display with discount percentage
- ✅ Image preview in list view
- ✅ Bulk actions (mark as featured, make available/unavailable)
- ✅ Inline gallery image management
- ✅ Inline reviews management
- ✅ Automatic slug generation

### Booking Admin
- ✅ Payment progress bar
- ✅ Color-coded payment and booking status
- ✅ Customer details in one view
- ✅ Bulk status updates

### Testimonial Admin
- ✅ Star rating display
- ✅ Bulk approve/unapprove actions
- ✅ Featured testimonials management

## Default Data to Add

After setting up, add the following in admin panel:

1. **Package Categories**: Adventure, Honeymoon, Family, Religious, Beach, Hill Station
2. **Site Settings**: Your contact details, social media links
3. **Packages**: At least 5-6 packages to showcase on homepage
4. **Testimonials**: 3-4 featured testimonials for homepage

## Customization

### Changing Colors
Edit `static/css/style.css` to change the color scheme:
- Primary color: `#667eea`
- Secondary color: `#764ba2`

### Adding More Pages
1. Create page in admin under "Pages"
2. Access via: http://127.0.0.1:8000/page/your-page-slug/

## Technologies Used
- **Backend**: Django 6.0.2
- **Frontend**: Bootstrap 5.3, Font Awesome 6.4
- **Database**: SQLite (can be changed to PostgreSQL for production)
- **Image Handling**: Pillow

## Support

For any issues or questions:
1. Check Django documentation: https://docs.djangoproject.com/
2. Review the code comments in views.py and models.py files

## Future Enhancements
- Payment gateway integration
- User authentication and user dashboard
- Package booking calendar
- Email notifications
- PDF invoice generation
- Multi-language support

## License
This project is created for educational purposes.

---

**Happy Traveling! ✈️**
