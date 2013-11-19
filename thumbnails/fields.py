from django.db.models import ImageField as DjangoImageField

from .files import ThumbnailedImageFile
from .processors import process


class ImageField(DjangoImageField):
    attr_class = ThumbnailedImageFile

    def __init__(self, *args, **kwargs):
        self.resize_original = kwargs.pop('resize_original', None)
        super(ImageField, self).__init__(self, *args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Process the source image through the defined processors.
        """
        file = getattr(model_instance, self.attname)

        if file and not file._committed:
            image_file = file
            if self.resize_original:
                image_file = process(file, self.resize_original)
            file.save(file.name, image_file, save=False)
        return file
