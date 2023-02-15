from django.db import models

# Create your models here.
from shortener.models import ShortURL


class ClickEventManager(models.Manager):
    def create_event(self, instance):
        if isinstance(instance, ShortURL):
            obj, created = self.get_or_create(shorturl=instance)
            obj.count += 1
            obj.save()
            return obj.count
        return None


class ClickEvent(models.Model):
    shorturl = models.OneToOneField(ShortURL, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)
