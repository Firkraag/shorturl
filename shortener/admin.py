from django.contrib import admin

# Register your models here.
from shortener.models import ShortURL

admin.site.register(ShortURL)
