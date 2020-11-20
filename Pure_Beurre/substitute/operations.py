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
from django.http import JsonResponse, HttpRequest, HttpResponse
#from substitute.models import Category, Aliment
from .models import Category, Aliment
lg.basicConfig(level=lg.INFO)


class Data:
    """
    Data class create an instance which centralizing
    all pure data coming from Openfoodfacts server.
    """
    def __init__(self):
        """
        Init constructor has two attributes:
        json_url_file : URLS file path needed to request OpFoFa server.
        big_data : Containing OpFoFa response, sliced and sorted.
        'big_data' is a dict.
        """

        self.json_url_file = ".\\substitute\\static\\substitute\\json\\urls.json"
        #self.json_url_file = ".\\static\\substitute\\json\\urls.json"
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

class DataEngine:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.categories = self.get_all_categories()
        self.aliments = self.get_aliments()
        self.big_data = self.formatting_result()

    def get_all_categories(self):
        all_categories = Category.objects.all()
        candidate = []
        for e in all_categories:
            if self.raw_data in str(e.name):
                candidate.append(e)
            if self.raw_data in str(e.id_name):
                candidate.append(e)
        return candidate

    def get_aliments(self):
        candidate = []
        for e in self.categories:
            try:
                aliment = Aliment.objects.get(tag=e.id)
                candidate.append(aliment)
            except Exception as e:
                lg.debug(e)
        all_aliments = Aliment.objects.all()
        for e in all_aliments:
            try:
                if self.raw_data in e.category:
                    candidate.append(e)
            except:
                lg.debug(e)
        return candidate

    def formatting_result(self):
        result = {}
        for i, e in enumerate(self.aliments):
            result[i] = {}
            result[i]["brand"] = e.brand
            result[i]["name"] = e.name
            result[i]["nutriscore"] = e.nutriscore
            result[i]["purchase_places"] = e.purchase_places
            result[i]["store"] = e.store
            result[i]["url"] = e.url
            result[i]["url_image"] = e.url_image
        return result

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
                print("\n*****")
                print(e_1)
                print(e_1.category)
                print("*****\n")
                indirect_aliment[e_1.id] = e_1
        return indirect_aliment

    def build_big_data(self):
        #big_data = {"direct": self.direct_aliment}
        #big_data = {"direct": self.direct_aliment,
        #            "indirect": self.indirect_aliment}
        big_data = {}
        big_data = self.direct_aliment
        big_data.update(self.indirect_aliment)
        return big_data


class DataAliment:
    def __init__(self, pk):
        self.aliment_id = pk
        self.aliment = self.get_aliment()

    def get_aliment(self):
        aliment = Aliment.objects.get(id=self.aliment_id)
        print(aliment)
        return aliment

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


def uptodate_formatting_categories(data):
    for i, e in enumerate(data["rcvd"]["categories"]):
        categories = {}
        categories["id"] = e["id"].replace("en:","")
        categories["name"] = e["product_name"]
        categories["url"] = e["url"]
        data["rcvd"]["essentials"]["categories"][i] = categories
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
                    data["rcvd"]["essentials"]["aliments"][k][i] = aliments
                except Exception as e:
                    lg.debug(e)
    return data


def get_data(data):
    data["rcvd"]["essentials"] = {}
    data["rcvd"]["essentials"]["aliments"] = {}
    data["rcvd"]["essentials"]["categories"] = {}
    return data


def get_aliments(data):
    """
    'get_aliments' method analyses each OpFoFa response
    and catches all aliments located in.
    These aliments are sorted by quality.
    Actually, some aliments info may not be provided.
    If it is so, this method set 'EMPTY' and 'NOT_PROVIDED'
    tags in the impacted field. All aliment information
    are stored in to the big data.
    Keys to find '["rcvd"]["aliments"]'.
    :param data:
    :return data:
    """
    list_r = ["product_name", "brands", "nutriscore_grade",
              "stores", "purchase_places", "url"]
    for url_name in data["sent"]["urls"].keys():
        data["rcvd"]["aliments"][url_name] = {}
        for i in range(0, len(data["rcvd"][url_name]["products"])):
            data["rcvd"]["aliments"][url_name][str(i)] = {}
            for element in list_r:
                if element in data["rcvd"][url_name]["products"][i]:
                    if data["rcvd"][url_name]["products"][i][element] == "":
                        data["rcvd"]["aliments"][url_name][str(i)][element]\
                            = "EMPTY"
                    else:
                        data["rcvd"]["aliments"][url_name][str(i)][element] = \
                            data["rcvd"][url_name]["products"][i][element]
                else:
                    data["rcvd"]["aliments"][url_name][str(i)][element]\
                        = "NOT_PROVIDED"
    return data


if __name__ == "__main__":


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
    session = DataSearch("biscuit")
    result = session.big_data
    print("\nfin d'operation\n")
    ##print("\n")
    ###############################