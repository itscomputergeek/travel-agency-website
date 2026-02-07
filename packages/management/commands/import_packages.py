import os
from pathlib import Path
from docx import Document
from django.core.management.base import BaseCommand
from django.core.files import File
from packages.models import Package, PackageCategory
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Import travel packages from Word documents'

    def handle(self, *args, **options):
        # Path to documents
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        docs_dir = base_dir / 'travle dcoument'

        if not docs_dir.exists():
            self.stdout.write(self.style.ERROR(f'Directory not found: {docs_dir}'))
            return

        # Create categories
        categories_map = self.create_categories()

        # Get all docx files
        docx_files = list(docs_dir.glob('*.docx'))
        self.stdout.write(self.style.SUCCESS(f'Found {len(docx_files)} package files'))

        imported_count = 0
        skipped_count = 0

        for docx_file in docx_files:
            try:
                # Extract destination and duration from filename
                filename = docx_file.stem
                package_data = self.parse_filename(filename)

                # Check if package already exists
                if Package.objects.filter(name=package_data['name']).exists():
                    self.stdout.write(self.style.WARNING(f'Skipped (exists): {package_data["name"]}'))
                    skipped_count += 1
                    continue

                # Read document content
                doc = Document(docx_file)
                content = self.extract_content(doc)

                # Determine category
                category = self.get_category(package_data['destination'], categories_map)

                # Create package
                package = Package.objects.create(
                    name=package_data['name'],
                    category=category,
                    short_description=f"Explore {package_data['destination']} in {package_data['duration_days']} days",
                    description=content.get('description', f"Experience the best of {package_data['destination']} with our carefully curated tour package."),
                    price=content.get('price', 10000),
                    original_price=content.get('original_price', None),
                    duration_days=package_data['duration_days'],
                    duration_nights=package_data['duration_nights'],
                    location=package_data['destination'],
                    destination_city=package_data['destination'],
                    destination_state=self.get_state(package_data['destination']),
                    destination_country='India',
                    inclusions=content.get('inclusions', 'Accommodation\nMeals as per itinerary\nTransportation\nSightseeing'),
                    exclusions=content.get('exclusions', 'Flight tickets\nPersonal expenses\nTravel insurance'),
                    itinerary=content.get('itinerary', self.generate_default_itinerary(package_data)),
                    highlights=content.get('highlights', ''),
                    hotel_type='3-Star',
                    meal_plan='Breakfast',
                    transport_mode='AC Vehicle',
                    available=True,
                    featured=True if imported_count < 8 else False,  # Mark first 8 as featured
                    popular=True if imported_count < 6 else False,
                )

                self.stdout.write(self.style.SUCCESS(f'[OK] Imported: {package.name}'))
                imported_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERROR] Error importing {docx_file.name}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\n=== Import Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Imported: {imported_count} packages'))
        self.stdout.write(self.style.WARNING(f'Skipped: {skipped_count} packages'))

    def create_categories(self):
        """Create package categories"""
        categories = {
            'Beach': ['Goa', 'Kerala', 'Kochi'],
            'Backwaters': ['Alleppey', 'Alappuzha'],
            'Hill Station': ['Ooty', 'Shimla', 'Coorg', 'Munnar'],
            'Religious': ['Jammu and Kashmir', 'Kashmir'],
            'Heritage': ['Rajasthan', 'Gujarat'],
            'City Tour': ['Calicut', 'Kochi'],
        }

        categories_map = {}
        for cat_name, destinations in categories.items():
            cat, created = PackageCategory.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'{cat_name} tour packages'}
            )
            for dest in destinations:
                categories_map[dest.lower()] = cat

        return categories_map

    def parse_filename(self, filename):
        """Extract package info from filename"""
        # Clean filename
        name = filename.replace('Tour Package', '').replace('tour package', '').strip()
        name = ' '.join(name.split())

        # Extract destination
        parts = name.split('-')
        if len(parts) > 1:
            destination = parts[0].strip()
            duration_part = parts[1].strip()
        else:
            # Try to parse without hyphen
            words = name.split()
            destination = words[0]
            duration_part = ' '.join(words[1:])

        # Extract duration
        duration_days = 1
        duration_nights = 0

        import re
        days_match = re.search(r'(\d+)\s*[Dd]ay', duration_part)
        nights_match = re.search(r'(\d+)\s*[Nn]ight', duration_part)

        if days_match:
            duration_days = int(days_match.group(1))
        if nights_match:
            duration_nights = int(nights_match.group(1))

        # Construct package name
        package_name = f"{duration_days}D/{duration_nights}N {destination} Tour Package"

        return {
            'name': package_name,
            'destination': destination,
            'duration_days': duration_days,
            'duration_nights': duration_nights,
        }

    def extract_content(self, doc):
        """Extract content from Word document"""
        full_text = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                full_text.append(text)

        content = '\n'.join(full_text)

        # Try to extract sections
        result = {
            'description': '',
            'inclusions': '',
            'exclusions': '',
            'itinerary': '',
            'highlights': '',
            'price': 10000,
        }

        # Simple extraction logic
        if content:
            result['description'] = content[:500] if len(content) > 500 else content

            # Look for common keywords
            if 'inclusion' in content.lower():
                idx = content.lower().find('inclusion')
                result['inclusions'] = content[idx:idx+300]

            if 'exclusion' in content.lower():
                idx = content.lower().find('exclusion')
                result['exclusions'] = content[idx:idx+300]

            if 'itinerary' in content.lower() or 'day 1' in content.lower():
                result['itinerary'] = content

        return result

    def get_category(self, destination, categories_map):
        """Get category for destination"""
        dest_lower = destination.lower()
        for key, category in categories_map.items():
            if key in dest_lower:
                return category

        # Default category
        default_cat, _ = PackageCategory.objects.get_or_create(
            name='Tour Packages',
            defaults={'description': 'General tour packages'}
        )
        return default_cat

    def get_state(self, destination):
        """Get state name for destination"""
        state_map = {
            'goa': 'Goa',
            'kerala': 'Kerala',
            'kochi': 'Kerala',
            'alleppey': 'Kerala',
            'calicut': 'Kerala',
            'ooty': 'Tamil Nadu',
            'shimla': 'Himachal Pradesh',
            'coorg': 'Karnataka',
            'kashmir': 'Jammu and Kashmir',
            'jammu': 'Jammu and Kashmir',
            'rajasthan': 'Rajasthan',
            'gujarat': 'Gujarat',
        }

        dest_lower = destination.lower()
        for key, state in state_map.items():
            if key in dest_lower:
                return state

        return 'India'

    def generate_default_itinerary(self, package_data):
        """Generate a default itinerary"""
        destination = package_data['destination']
        days = package_data['duration_days']

        itinerary = []
        for day in range(1, days + 1):
            if day == 1:
                itinerary.append(f"Day {day}: Arrival at {destination}")
                itinerary.append("- Check-in to hotel")
                itinerary.append("- Evening at leisure")
            elif day == days:
                itinerary.append(f"\nDay {day}: Departure")
                itinerary.append("- Check-out from hotel")
                itinerary.append("- Transfer to airport/station")
            else:
                itinerary.append(f"\nDay {day}: {destination} Sightseeing")
                itinerary.append("- Local sightseeing tours")
                itinerary.append("- Visit major attractions")

        return '\n'.join(itinerary)
