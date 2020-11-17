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

        data = fill_target()
        fill_category(data, "categories")
        fill_aliment(data, "aliments")










        #for e in list_t:
        #    raw_data = e
        #    session = Data(raw_data)
        #    data =session.big_data
        #    print("\n" + "*" * 10)
        #    print("STORE DATA")
        #    print("*" * 10 + "\n")
        #    data = data["rcvd"]["essentials"]
        #    # print(data)
        #    check_aliments = "aliments"
        #    check_categories = "categories"
        #    for k, v in data.items():
        #        # print(k)
        #        if k == check_categories:
        #            # elif k == check_categories and "id" in v.keys():
        #            # print(k)
        #            for k_1, v_1 in v.items():
        #                id_name = v_1["id"]
        #                name = v_1["name"]
        #                url = v_1["url"]
        #                the_categories = CategoryValue(
        #                    id_name=id_name,
        #                    name=name,
        #                    url=url
        #                )
        #                # print("\n" + "*" * 10)
        #                # print("Lancement sauvegarde category")
        #                # print("*" * 10 + "\n")
        #                the_categories.store_items()
        #            # print("\n**** categories creees ****\n")
        #    for k, v in data.items():
        #        if k == check_aliments:
        #            for k_1, v_1 in v.items():
        #                # print(v_1["brand"])
        #                brand = v_1["brand"]
        #                product_name = v_1["product_name"]
        #                categories = v_1["categories"]
        #                nutriscore = v_1["nutriscore"]
        #                purchase_place = str(v_1["purchase_place"])
        #                store = str(v_1["store"])
        #                url = v_1["url"]
        #                url_image = v_1["images"]["front"]["small"]["fr"]
        #                the_aliments = AlimentValue(
        #                    brand=brand,
        #                    product_name=product_name,
        #                    category=categories,
        #                    nutriscore=nutriscore,
        #                    purchase_place=purchase_place,
        #                    store=store,
        #                    url=url,
        #                    url_image=url_image
        #                )
        #                # print("\n" + "*" * 10)
        #                # print("Lancement sauvegarde aliment")
        #                # print("*" * 10 + "\n")
        #                the_aliments.store_items()
        #        else:
        #            print("KO")

def open_json_file(json_file):
    """'open_json_file' method read a given json file.
    It returns the content file into a dict."""
    with open(json_file) as file:
        data = json.load(file)
    return data

def fill_category(data, check):
    for k, v in data["cleaned_categories"].items():
        #if k == check:
        #for k_1, v_1 in v.items():
        id_name = v["id"]
        name = v["name"]
        url = v["url"]
        the_categories = CategoryValue(
            id_name=id_name,
            name=name,
            url=url
        )
        # print("\n" + "*" * 10)
        # print("Lancement sauvegarde category")
        # print("*" * 10 + "\n")
        the_categories.store_items()
        # print("\n**** categories creees ****\n")

def fill_aliment(data, check):
    for k, v in data["rcvd"]["essentials"]["aliments"].items():
        #if k == check:
        for k_1, v_1 in v.items():
            for k_2, v_2 in v.items():
                # print(v_1["brand"])
                brand = v_2["brand"]
                product_name = v_2["product_name"]
                categories = v_2["categories"]
                nutriscore = v_2["nutriscore"]
                purchase_place = str(v_2["purchase_place"])
                store = str(v_2["store"])
                url = v_2["url"]
                url_image = v_2["images"]["front"]["small"]["fr"]
                the_aliments = AlimentValue(
                    brand=brand,
                    product_name=product_name,
                    category=categories,
                    nutriscore=nutriscore,
                    purchase_place=purchase_place,
                    store=store,
                    url=url,
                    url_image=url_image
                )
                # print("\n" + "*" * 10)
                # print("Lancement sauvegarde aliment")
                # print("*" * 10 + "\n")
                the_aliments.store_items()

def fill_target():
        session = Data()
        data = session.big_data
        print("\n" + "*" * 10)
        print("STORE DATA")
        print("*" * 10 + "\n")
        #data = data["rcvd"]["essentials"]
        # print(data)
        #check_aliments = "aliments"
        #check_categories = "categories"
        return data
