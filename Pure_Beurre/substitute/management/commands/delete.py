from django.core.management.base import BaseCommand
from substitute.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        all_categories = Category.objects.all()
        all_aliments = Aliment.objects.all()
        all_categories.delete()
        all_aliments.delete()