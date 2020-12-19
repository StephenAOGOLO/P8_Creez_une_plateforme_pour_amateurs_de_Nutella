"""
Welcome to the API Operations module, 'api_operations.py'.
This module is composed of 'Data' class.
three methods are defined to retrieve and store data
coming from OpFoFa - OpenFoodFacts server.
ten functions are defined to slice and sort the data
needed for each packages module.
"""
# -*- coding: utf-8 -*-
import logging as lg
import json
import requests
from .models import *
from .Values import *
lg.basicConfig(level=lg.INFO)
BASE_DIR = Path(__file__).resolve().parent.parent


class Data:
    """
    Data class create an instance which centralizing
    all pure data coming from Openfoodfacts server.
    """
    def __init__(self, urls_json=BASE_DIR + "\\substitute\\static\\substitute\\json\\urls.json"):
    #def __init__(self, urls_json=".\\substitute\\static\\substitute\\json\\urls.json"):
        """
        Init constructor has two attributes:
        json_url_file : URLS file path needed to request OpFoFa server.
        big_data : Containing OpFoFa response, sliced and sorted.
        'big_data' is a dict.
        """

        self.json_url_file = urls_json
        self.big_data = self.load_api_data()

    def load_api_data(self):
        """
        'Load_api_data' method is containing every steps of
         getting, slicing and sorting
         before the data providing.
         """

        all_data = self.request_urls()
        all_data = self.response_urls(all_data)
        all_data = get_data(all_data)
        all_data = formatting_data(all_data)
        return all_data

    def open_json_file(self):
        """'open_json_file' method read a given json file.
        It returns the content file into a dict."""
        with open(self.json_url_file) as file:
            data = json.load(file)
        return data

    def get_target(self, all_data):
        return all_data["sent"]["urls"]["target"]

    def request_urls(self):
        """
        'request_urls' method adds url requests into the big data
        :param all_data:
        :return all_data:
        """
        all_data = {"sent": {}, "rcvd": {}}
        all_data["sent"]["urls"] = self.open_json_file()
        self.target = self.get_target(all_data)
        return all_data

    def response_urls(self, all_data):
        """
        'response_urls' method execute each url request.
        Each response is stored into the big data.
        :param all_data:
        :return all_data:
        """
        print("\nCollecte des données OpenFoodFacts...\n")
        for url_name, url in all_data["sent"]["urls"].items():
            if url_name == "aliments":
                all_data["rcvd"][url_name] = {}
                for raw_data in self.target:
                    all_data["rcvd"][url_name][raw_data] = {}
                    new_url = url + raw_data
                    response = requests.get(new_url)
                    response = json.loads(response.content.decode("utf-8"))
                    response = response["products"]
                    all_data["rcvd"][url_name][raw_data] = response
        for url_name, url in all_data["sent"]["urls"].items():
            if url_name == "categories":
                response = requests.get(url)
                response = json.loads(response.content.decode("utf-8"))
                response = response["tags"]
                all_data["rcvd"][url_name] = response
            elif url_name == "target":
                response = url
                all_data["rcvd"][url_name] = response
        return all_data


class DataSearch:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.direct_aliment = self.get_direct_aliment()
        self.indirect_aliment = self.get_indirect_aliment()
        self.big_data = self.build_big_data()

    def get_direct_aliment(self):
        direct_aliment = {}
        aliments = Aliment.objects.filter(name__icontains=self.raw_data)
        for e in aliments:
            direct_aliment[e.id] = e
        return direct_aliment

    def get_indirect_aliment(self):
        indirect_aliment = {}
        aliments = []
        categories = Category.objects.filter(name__icontains=self.raw_data)
        for e in categories:
            aliment = Aliment.objects.filter(category__contains=e.id_name)
            aliments.append(aliment)
        for e in aliments:
            for e_1 in e:
                indirect_aliment[e_1.id] = e_1
        return indirect_aliment

    def build_big_data(self):
        big_data = {}
        big_data = self.direct_aliment
        big_data.update(self.indirect_aliment)
        big_data = sort_big_data(big_data)
        return big_data


class DataSave:
    def __init__(self, aliment, substitute, customer):
        self.aliment = aliment
        self.substitute = substitute
        self.customer = customer

    def store_data(self):
        the_historic = HistoricValue(self.aliment, self.substitute, self.customer)
        the_historic.store_items()


class DataAliment:
    def __init__(self, pk):
        self.aliment_id = pk
        self.aliment = self.get_aliment()

    def get_aliment(self):
        aliment = Aliment.objects.get(id=self.aliment_id)
        print(aliment)
        return aliment



def open_js_file(js_file):
    """'open_json_file' method read a given json file.
    It returns the content file into a dict."""
    with open(js_file) as file:
        data = json.load(file)
    return data


def is_entry_empty(text):
    """ This function checks if no words is given for search """
    status = False
    text = text.strip()
    if text == "":
        status = True
        text = "Pouvez-vous reformuler votre saisie pour ce produit"
    report = {"status": status, "text": text}
    return report


def secure_text(text, js_file=".\\substitute\\static\\substitute\\json\\xss.json"):
    """ This function handles XSS breaches """
    bad_words = open_js_file(js_file)
    for c_1 in bad_words["xss"]:
        if c_1 in text:
            text = text.replace(c_1, "")
    return text


def get_historic(customer):
    the_historic = Historic.objects.filter(user_id=customer.id)
    for e in the_historic:
        e.aliment.nutriscore = set_nutriscore_tag(e.aliment.nutriscore)
        e.substitute.nutriscore = set_nutriscore_tag(e.substitute.nutriscore)
    return the_historic


def sort_big_data(big_data):
    new_data = sorted(big_data.items(), key=lambda t: t[1].nutriscore)
    big_data = {}
    for e in new_data:
        big_data[e[0]] = e[1]
    return big_data


def formatting_data(data):
    print("\nMise en forme des données collectées..\n")
    data = formatting_aliments(data)
    data = formatting_categories(data)
    data = cleaning_categories(data)
    print("\nCollecte et mise en forme des données terminées.\n")
    return data


def cleaning_categories(data):
    cleaner = data["rcvd"]["essentials"]["aliments"]
    cleaned = data["rcvd"]["essentials"]["categories"]
    list_big = []
    list_cleaner = []
    dict_cleaned = {}
    for k, v in cleaner.items():
        for k_1, v_1 in v.items():
            for e in v_1["categories"]:
                list_big.append(e)
    for e in list_big:
        if not e in list_cleaner:
            list_cleaner.append(e)
    data["cleaner_categories"] = list_cleaner
    for k, v in cleaned.items():
        if not v["id"] in list_cleaner:
            continue
        dict_cleaned[k] = v
    data["cleaned_categories"] = dict_cleaned
    return data



def formatting_categories(data):
    for i, e in enumerate(data["rcvd"]["categories"]):
        categories = {}
        check_data = "known"
        if check_data in e.keys() and e[check_data] == 1:
            categories["id"] = e["id"].replace("en:","")
            categories["name"] = e["name"]
            categories["url"] = e["url"]
            data["rcvd"]["essentials"]["categories"][i] = categories
    return data


def formatting_aliments(data):
    aliments = {}
    for k, v in data["rcvd"]["aliments"].items():
        data["rcvd"]["essentials"]["aliments"][k] = {}
        for i, e in enumerate(v):
            aliments = {}
            check_data = "nutriscore_data"
            if check_data in e.keys():
                try:
                    aliments["nutriscore"] = e["nutriscore_data"]["grade"]
                    aliments["url"] = e["url"]
                    aliments["product_name"] = e["product_name_fr"]
                    aliments["categories"] = [e_1.replace("en:", "") for e_1 in e["categories_hierarchy"]]
                    aliments["brand"] = e["brands"].replace(",",", ")
                    aliments["purchase_place"] = e["purchase_places"].replace(",",", ")
                    aliments["store"] = e["stores"].replace(",",", ")
                    aliments["images"] = e["selected_images"]
                    aliments["nutriments_image"] = e["selected_images"]["nutrition"]["display"]["fr"]
                    aliments["nutriments_energy_kj"] = e["nutriments"]["energy-kj"]
                    aliments["nutriments_energy_kj_unit"] = e["nutriments"]["energy-kj_unit"]
                    aliments["nutriments_energy_kcal"] = e["nutriments"]["energy-kcal"]
                    aliments["nutriments_energy_kcal_unit"] = e["nutriments"]["energy-kcal_unit"]
                    data["rcvd"]["essentials"]["aliments"][k][i] = aliments
                except Exception as e:
                    lg.debug(e)
    return data


def get_data(data):
    data["rcvd"]["essentials"] = {}
    data["rcvd"]["essentials"]["aliments"] = {}
    data["rcvd"]["essentials"]["categories"] = {}
    return data


def set_nutriscore_tag(tag):
    new_tag = '/static/substitute/png/{}_nutriscore_good.png'.format(tag)
    return new_tag


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
            try:
                brand = v_1["brand"]
                product_name = v_1["product_name"]
                categories = v_1["categories"]
                nutriscore = v_1["nutriscore"]
                purchase_place = str(v_1["purchase_place"])
                store = str(v_1["store"])
                url = v_1["url"]
                url_image = v_1["images"]["front"]["small"]["fr"]
                nutriments_image = v_1["nutriments_image"]
                nutriments_energy_kj = v_1["nutriments_energy_kj"]
                nutriments_energy_kj_unit = v_1["nutriments_energy_kj_unit"]
                nutriments_energy_kcal = v_1["nutriments_energy_kcal"]
                nutriments_energy_kcal_unit = v_1["nutriments_energy_kcal_unit"]
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
            except Exception as e:
                print(e)

#if __name__ == "__main__":

    ##### TEST on Data class #####
    #session = Data()
    #result = session.big_data
    #print("\nfin d'operation\n")
    ##print("\n")
    ###############################

    ##### TEST on DataEngine class #####
    #session = DataEngine("biscuit")
    #result = session.big_data
    #print("\nfin d'operation\n")
    ##print("\n")
    ###############################

    ##### TEST on DataSearch class #####
    #from Pure_Beurre.substitute.models import Aliment
    #import Pure_Beurre.substitute.models
    #session = DataSearch("biscuit")
    #result = session.big_data
    #print("\nfin d'operation\n")
    ##print("\n")
    ###############################