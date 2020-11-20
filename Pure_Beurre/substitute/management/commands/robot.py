from django.core.management.base import BaseCommand
from substitute.models import *
from substitute.operations import Data
from substitute.Values import AlimentValue, CategoryValue
import json



class Command(BaseCommand):

    #def handle(self, *args, **options):
    #    self.stdout.write(self.style.SUCCESS("ROBOT WORKS !!!"))
    all_categories = Category.objects.all()
    all_aliments = Aliment.objects.all()
    all_categories.delete()
    all_aliments.delete()
    def handle(self, *args, **options):
        session = Data()
        data = session.big_data
        fill_category(data)
        fill_aliment(data)
        self.stdout.write(self.style.SUCCESS("ROBOT OVER !!!"))


def open_json_file(json_file):
    """'open_json_file' method read a given json file.
    It returns the content file into a dict."""
    with open(json_file) as file:
        data = json.load(file)
    return data

def fill_category(data,):
    for k, v in data["cleaned_categories"].items():
        id_name = v["id"]
        name = v["name"]
        url = v["url"]
        the_categories = CategoryValue(
            id_name=id_name,
            name=name,
            url=url
        )
        the_categories.store_items()


def fill_aliment(data):
    for k, v in data["rcvd"]["essentials"]["aliments"].items():
        for k_1, v_1 in v.items():
            for k_2, v_2 in v.items():
                brand = v_2["brand"]
                product_name = v_2["product_name"]
                categories = v_2["categories"]
                nutriscore = v_2["nutriscore"]
                purchase_place = str(v_2["purchase_place"])
                store = str(v_2["store"])
                url = v_2["url"]
                url_image = v_2["images"]["front"]["small"]["fr"]

                nutriments_image = v_2["nutriments_image"]
                nutriments_energy_kj = v_2["nutriments_energy_kj"]
                nutriments_energy_kj_unit = v_2["nutriments_energy_kj_unit"]
                nutriments_energy_kcal = v_2["nutriments_energy_kcal"]
                nutriments_energy_kcal_unit = v_2["nutriments_energy_kcal_unit"]
                the_aliments = AlimentValue(
                    brand=brand,
                    product_name=product_name,
                    category=categories,
                    nutriscore=nutriscore,
                    purchase_place=purchase_place,
                    store=store,
                    url=url,
                    url_image=url_image,
                    energy_img=nutriments_image,
                    energy_kj=nutriments_energy_kj,
                    energy_kj_unit=nutriments_energy_kj_unit,
                    energy_kcal=nutriments_energy_kcal,
                    energy_kcal_unit=nutriments_energy_kcal_unit
                )
                the_aliments.store_items()


