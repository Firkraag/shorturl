from django.core.management.base import BaseCommand

from shortener.models import ShortURL


class Command(BaseCommand):
    help = 'Refresh all shortcodes'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)

    def handle(self, *args, **options):
        # print(options)
        return ShortURL.objects.refresh_shortcodes(options['items'])
