from django.core.exceptions import ValidationError
import os


def allow_only_images_valiadator(value):

    # For this custom validator to work we should change the input from "ImageField" to "FileInput"
    # If we dont change it then the usual validation error only will show
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensios = ['.png','.jpg', '.jpeg']
    if not ext.lower() in valid_extensios:
        raise ValidationError('Unsupported file extension. Allowed  extensions : ' + str(valid_extensios))