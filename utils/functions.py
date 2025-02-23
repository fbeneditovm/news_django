from django.core.exceptions import ValidationError


def validate_image_file(value):
    import os
    filesize = value.size
    if filesize > 10485760:  # 10MB
        raise ValidationError("Max file size is 10MB")
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions are: jpg, jpeg, png, gif')
