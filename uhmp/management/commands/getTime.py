from django.core.management.base import BaseCommand, CommandError
from uhmp import views

class Command(BaseCommand):
    args = ''
    help = 'Updates the Hist Objects.'

    def handle(self, *args, **options):
	print views.getTime()
