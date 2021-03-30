import os
import logging

from django.conf import settings
from django.core.files import File

from wagtail.images import get_image_model

logger = logging.getLogger("fake users:")
Image = get_image_model()

def create_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

create_dir_if_not_exists(settings.MEDIA_ROOT)
create_dir_if_not_exists(settings.DOWNLOADS_ROOT)
create_dir_if_not_exists(settings.IMAGE_DOWNLOADS_DIR)
create_dir_if_not_exists(settings.AVATAR_DOWNLOADS_DIR)

def create_wagtail_image(filename):
    filepath = os.path.join(settings.IMAGE_DOWNLOADS_DIR, filename)
    with open(filepath, "rb") as file:
        image_file = File(file)
        return Image.objects.create(file=image_file, title=filename)


def create_wagtail_images():
    images = []
    files = os.listdir(settings.IMAGE_DOWNLOADS_DIR)
    for file in files:
        images.append(create_wagtail_image(file))
        logger.info(
            f'Successfully created image: {file}'
        )
    return images
