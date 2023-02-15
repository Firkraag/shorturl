from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from .validators import validate_url


class SubmitUrlForm(forms.Form):
    url = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Enter the link here"}))

    def clean_url(self):
        url = self.cleaned_data['url']
        url_validator = URLValidator()
        try:
            url_validator(url)
        except ValidationError:
            url = "https://" + url
            url_validator(url)
        return url
