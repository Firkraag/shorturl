from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_url(url):
    url_validator = URLValidator()
    try:
        url_validator(url)
    except ValidationError:
        url_validator("http://" + url)


def validate_dot_com(url):
    if "com" not in url:
        raise ValidationError("This is not valid because of no .com")
