import os
import uuid

from PIL import Image


def watermark_with_transparency(input_image_path,
                                watermark_image_path,
                                position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path).convert('RGBA')
    filename = str(input_image_path)
    extension = os.path.splitext(filename)[1]
    filepath = f'images/{uuid.uuid4()}{extension}'
    base_image.paste(watermark, position)
    base_image.save(f'media/{filepath}')
    return filepath
