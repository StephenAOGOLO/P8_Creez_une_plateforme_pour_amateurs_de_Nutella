""" This module is a manage.py command
 used for fill the website database.  """
from django.core.management.base import BaseCommand
from substitute.models import *
from substitute.operations import *
# -*- coding: utf-8 -*-


class Command(BaseCommand):
    """ This class erases all data from Text,
     Category and Aliment Tables.
    """
    print("\nPréparation de la base de données en cours...\n")
    all_text = Text.objects.all()
    all_text.delete()
    print("\nTable 'Text' prête.\n")
    all_categories = Category.objects.all()
    all_categories.delete()
    print("\nTable 'Category' prête.\n")
    all_aliments = Aliment.objects.all()
    all_aliments.delete()
    print("\nTable 'Aliment' prête.\n")

    def handle(self, *args, **options):
        """  This method runs the following actions:
            - To fill Text Table
            - To fill Category Table
            - To fill Aliment Table
        """
        self.stdout.write(self.style.SUCCESS("Mise à jour de la base de données en cours..."))
        fill_text()
        session = Data()
        data = session.big_data
        fill_category(data)
        fill_aliment(data)
        self.stdout.write(self.style.SUCCESS("Mise à jour de la base de données terminé."))
