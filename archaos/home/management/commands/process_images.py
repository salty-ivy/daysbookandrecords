from django.core.management.base import BaseCommand
from wagtail.images.models import Image


class Command(BaseCommand):
    help = 'Fetch all images and generate renditions'

    def handle(self, *args, **kwargs):
        # Fetch all images
        all_images = Image.objects.all()

        # Iterate through each image and run `get_renditions`
        for image in all_images:
            try:
                # Example usage of get_rendition
                rendition = image.get_rendition('max-165x165')
                self.stdout.write(self.style.SUCCESS(f"Image: {image.title}, Rendition URL: {rendition.url}"))
            except Exception as e:
                # If an error occurs, print the original image URL and the error
                self.stderr.write(self.style.ERROR(f"Error processing image {image.title} (URL: {image.file.url}): {e}"))
                # Delete all renditions for this image
                # self.delete_renditions(image)

                # Delete the original image file
                # image.delete()
                # self.stdout.write(self.style.WARNING(f"Deleted image {image.title} and all its renditions"))

    def delete_renditions(self, image):
        # Delete all renditions of the image
        renditions = image.renditions.all()
        for rendition in renditions:
            rendition.delete()
            self.stdout.write(self.style.WARNING(f"Deleted rendition: {rendition.file.url}"))
