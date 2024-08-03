from os import path

from django.conf import settings
from PIL import Image


def resize_image(image, new_width=840):
        image_full_path = path.join(settings.MEDIA_ROOT, image.name)
        pillow_image = Image.open(image_full_path)
        original_width, original_height = pillow_image.size

        if original_height < new_width:
            pillow_image.close()
            return

        new_height = round((new_width * original_height) / original_width)
        new_image = pillow_image.resize(
            (new_width, new_height), Image.Resampling.LANCZOS
        )
        new_image.save(
            image_full_path,
            optimize=True,
            quality=60
        )
