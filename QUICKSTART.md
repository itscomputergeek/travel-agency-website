# Quick Start Guide

## Step-by-Step Setup

### 1. Create Admin Account
```bash
python manage.py createsuperuser
```
- Enter username (e.g., `admin`)
- Enter email (e.g., `admin@example.com`)
- Enter password (minimum 8 characters)
- Confirm password

### 2. Run the Server
```bash
python manage.py runserver
```

### 3. Access the Website
- **Website**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### 4. Add Content in Admin Panel

#### A. Create Site Settings (Do this first!)
1. Login to admin panel
2. Click "Site Settings" → "Add Site Settings"
3. Fill in:
   - Site Name: "Your Travel Agency Name"
   - Contact Email: your@email.com
   - Contact Phone: +91 XXXXXXXXXX
   - Address: Your full address
   - Social Media URLs (optional)
   - Hero Title: "Explore the World with Us"
   - Hero Subtitle: "Your tagline here"
4. Click "Save"

#### B. Create Package Categories
1. Go to "Package Categories" → "Add Package Category"
2. Add these categories:
   - Adventure
   - Honeymoon
   - Family Tour
   - Religious Tour
   - Beach Vacation
   - Hill Station
3. Save each one

#### C. Add Your First Package
1. Go to "Packages" → "Add Package"
2. Fill in all fields:
   - **Name**: e.g., "5D/4N Goa Beach Holiday"
   - **Category**: Select one
   - **Short Description**: Brief one-liner
   - **Description**: Detailed package description
   - **Price**: e.g., 15000
   - **Original Price**: e.g., 20000 (for discount)
   - **Duration**: Days: 5, Nights: 4
   - **Location**: Full location name
   - **Destination City**: e.g., "Goa"
   - **Destination Country**: "India"
   - **Featured Image**: Upload main package image
   - **Inclusions** (one per line):
     ```
     Accommodation in 3-star hotel
     Daily breakfast
     Airport transfers
     Sightseeing tours
     ```
   - **Exclusions** (one per line):
     ```
     Flight tickets
     Lunch and dinner
     Personal expenses
     ```
   - **Itinerary**: Write day-wise plan
   - **Check "Featured"** to show on homepage
   - **Check "Available"**
3. Click "Save and add another" to add more packages

#### D. Add Testimonials
1. Go to "Testimonials" → "Add Testimonial"
2. Fill in:
   - Customer Name
   - Package Name
   - Rating: 5 stars
   - Title: Short review headline
   - Review: Full review text
   - Check "Approved" and "Featured"
3. Add 3-4 testimonials

### 5. View Your Website
Open http://127.0.0.1:8000/ and see your travel agency website live!

## Quick Tips

- Add at least **6-8 packages** for best homepage display
- Mark **4-6 packages as "Featured"** for homepage
- Add **3-4 testimonials** as featured
- Upload good quality images (recommended: 1200x800px)
- Fill all package details for better user experience

## Default Admin Credentials (Change after first login!)
- Username: (what you created)
- Password: (what you created)

## Need Help?
- Check README.md for detailed documentation
- All models are documented with help text
- Admin panel has inline help for each field

## Common Commands
```bash
# Run server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Make migrations (after model changes)
python manage.py makemigrations
python manage.py migrate

# Collect static files (for production)
python manage.py collectstatic
```

---

**You're all set! Start adding packages and customize your travel agency website.** 🚀
