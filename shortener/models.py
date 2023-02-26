from django.conf import settings
from django.db import models
from django.urls import reverse

from .utils import create_shortcode
from .validators import validate_url

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)


# Create your models here.
class ShortURLManager(models.Manager):
    def get_queryset(self):
        return super(ShortURLManager, self).get_queryset().filter(active=True)

    def refresh_shortcodes(self, items=None):
        qs = super(ShortURLManager, self).get_queryset()
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items]
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)


class ShortURL(models.Model):
    url = models.CharField(max_length=200, validators=[validate_url], unique=True)
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects = ShortURLManager()

    def __str__(self):
        return str(self.url)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.shortcode is None or self.shortcode == '':
            self.shortcode = create_shortcode(self)
        super(ShortURL, self).save(force_insert, force_update, using, update_fields)

    def get_short_url(self):
        return reverse("scode", kwargs={"shortcode": self.shortcode})
