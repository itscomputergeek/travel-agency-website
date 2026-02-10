import os
import time
import requests
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from packages.models import Package
from decouple import config


class Command(BaseCommand):
    help = 'Fetch and assign images to packages from Pexels API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--api-key',
            type=str,
            help='Pexels API key (or set PEXELS_API_KEY environment variable)',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of packages to process (for testing)',
        )
        parser.add_argument(
            '--images-per-package',
            type=int,
            default=5,
            help='Number of images to fetch per package (default: 5)',
        )

    def handle(self, *args, **options):
        # Get API key from argument or environment
        api_key = options.get('api_key') or config('PEXELS_API_KEY', default=None)

        if not api_key:
            self.stdout.write(self.style.ERROR(
                'ERROR: Pexels API key is required!\n'
                'Get a free API key at: https://www.pexels.com/api/\n'
                'Then set it as environment variable: PEXELS_API_KEY=your_key\n'
                'Or pass it via: --api-key=your_key'
            ))
            return

        images_per_package = options.get('images_per_package', 5)
        limit = options.get('limit')

        # Get packages that need images
        packages = Package.objects.all()
        if limit:
            packages = packages[:limit]

        total_packages = packages.count()
        self.stdout.write(self.style.SUCCESS(f'Found {total_packages} packages'))

        processed = 0
        skipped = 0
        errors = 0

        for package in packages:
            try:
                # Check if package already has images
                if package.featured_image and package.image_2 and package.image_3:
                    self.stdout.write(self.style.WARNING(
                        f'Skipped (has images): {package.name}'
                    ))
                    skipped += 1
                    continue

                self.stdout.write(f'Processing: {package.name}')

                # Fetch images from Pexels
                images = self.fetch_images(
                    api_key,
                    package.destination_city,
                    images_per_package
                )

                if not images:
                    self.stdout.write(self.style.WARNING(
                        f'  No images found for: {package.destination_city}'
                    ))
                    errors += 1
                    continue

                # Download and assign images to package
                self.assign_images_to_package(package, images)

                self.stdout.write(self.style.SUCCESS(
                    f'  Assigned {len(images)} images to {package.name}'
                ))
                processed += 1

                # Rate limiting: Sleep to avoid hitting API limits
                time.sleep(1)

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'  ERROR processing {package.name}: {str(e)}'
                ))
                errors += 1

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Image Fetching Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Processed: {processed} packages'))
        self.stdout.write(self.style.WARNING(f'Skipped: {skipped} packages'))
        self.stdout.write(self.style.ERROR(f'Errors: {errors} packages'))

    def fetch_images(self, api_key, query, per_page=5):
        """Fetch images from Pexels API"""
        url = 'https://api.pexels.com/v1/search'

        headers = {
            'Authorization': api_key
        }

        params = {
            'query': f'{query} travel tourism',
            'per_page': per_page,
            'orientation': 'landscape',
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            images = []
            for photo in data.get('photos', []):
                images.append({
                    'url': photo['src']['large'],
                    'photographer': photo['photographer'],
                })

            return images

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'API Error: {str(e)}'))
            return []

    def assign_images_to_package(self, package, images):
        """Download and assign images to package fields"""

        # Map images to package fields
        image_fields = ['featured_image', 'image_2', 'image_3', 'image_4', 'image_5']

        for idx, image_data in enumerate(images[:5]):
            if idx >= len(image_fields):
                break

            field_name = image_fields[idx]

            # Skip if field already has an image
            current_value = getattr(package, field_name)
            if current_value:
                continue

            try:
                # Download image
                img_url = image_data['url']
                response = requests.get(img_url, timeout=10)
                response.raise_for_status()

                # Save to temporary file (Python 3.14 compatible)
                img_temp = NamedTemporaryFile()
                img_temp.write(response.content)
                img_temp.flush()
                img_temp.seek(0)

                # Generate filename
                filename = f'{package.slug}_{idx + 1}.jpg'

                # Assign to package field
                field = getattr(package, field_name)
                field.save(filename, File(img_temp), save=False)

                self.stdout.write(f'    Downloaded: {filename}')

            except Exception as e:
                self.stdout.write(self.style.WARNING(
                    f'    Failed to download image {idx + 1}: {str(e)}'
                ))
                continue

        # Save package with all new images
        package.save()
