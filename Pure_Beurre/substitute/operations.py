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
from substitute.models import Category, Aliment



class DataEngine:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.categories = self.get_all_categories()
        self.aliments = self.get_aliments()
        self.big_data = self.formatting_result()

    def get_all_categories(self):
        all_categories = Category.objects.all()
        #print(all_categories)
        candidate = []
        #print("***")
        #print(self.raw_data)
        #print("***")
        for e in all_categories:
            #print(e.name)
            if self.raw_data in str(e.name):
                candidate.append(e)
            if self.raw_data in str(e.id_name):
                candidate.append(e)
        #print(candidate)
        return candidate

    def get_aliments(self):
        candidate = []
        #print(self.categories)
        for e in self.categories:
            #print(e.id)
            try:
                aliment = Aliment.objects.get(tag=e.id)
                candidate.append(aliment)
            except Exception as e:
                print(e)
        all_aliments = Aliment.objects.all()
        for e in all_aliments:
            try:
                if self.raw_data in e.category:
                    candidate.append(e)
            except:
                print(e)
        #print(candidate)
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





class Data:
    """
    Data class create an instance which centralizing
    all pure data coming from Openfoodfacts server.
    """
    def __init__(self, raw_data):
        """
        Init constructor has two attributes:
        json_url_file : URLS file path needed to request OpFoFa server.
        big_data : Containing OpFoFa response, sliced and sorted.
        'big_data' is a dict.
        """
        self.raw_data = raw_data
        self.json_url_file = ".\\substitute\\static\\substitute\\json\\urls.json"
        #self.json_url_file = ".\\static\\substitute\\json\\urls.json"
        self.big_data = self.load_api_data()

    def load_api_data(self):
        """
        'Load_api_data' method is containing every steps of
         getting, slicing and sorting
         before the data providing.
         """
        all_data = {"sent": {}, "rcvd": {}}
        all_data = self.request_urls(all_data)
    #    print("La récupération des données depuis le serveur OpenFoodFacts est en cours...")
        all_data = self.response_urls(all_data)
    #    print("Récupération des données terminée OpenFoodFacts avec succès")
    #    print("Organisation des données en cours...")
        all_data = get_data(all_data)
        all_data = formatting_data(all_data)
    #    all_data = get_aliments(all_data)
    #    print("Préparation des données pour l'interface en cours...")
    #    print("Préparation des données pour la base de données en cours...")
    #    all_data = all_rows(all_data)
    #    all_data = all_categories(all_data)
    #    all_data = prepare_sql_values(all_data)
    #    all_data = prepare_hmi_values(all_data)
    #    all_data = classify_ihm_values(all_data)
    #    print("Préparation des données terminée!!!")
    #    print("Préparation des données terminée!!!")
    #    print("Initialisation du système terminée avec succès.\n")
        return all_data

    def open_json_file(self):
        """'open_json_file' method read a given json file.
        It returns the content file into a dict."""
        with open(self.json_url_file) as file:
            data = json.load(file)
        return data

    def request_urls(self, all_data):
        """
        'request_urls' method adds url requests into the big data
        :param all_data:
        :return all_data:
        """
        all_data["sent"]["urls"] = self.open_json_file()
        return all_data

    def response_urls(self, all_data):
        """
        'response_urls' method execute each url request.
        Each response is stored into the big data.
        :param all_data:
        :return all_data:
        """
        for url_name, url in all_data["sent"]["urls"].items():
            if url_name == "aliments":
                url = url + self.raw_data
                response = requests.get(url)
                response = json.loads(response.content.decode("utf-8"))
                response = response["products"]
            elif url_name == "categories":
                response = requests.get(url)
                response = json.loads(response.content.decode("utf-8"))
                response = response["tags"]
            all_data["rcvd"][url_name] = response
        return all_data


def formatting_data(data):
    data = formatting_aliments(data)
    data = formatting_categories(data)
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
    for i, e in enumerate(data["rcvd"]["aliments"]):
        aliments = {}
        check_data = "nutriscore_data"
        if check_data in e.keys():
            aliments["nutriscore"] = e["nutriscore_data"]["grade"]
            aliments["url"] = e["url"]
            aliments["product_name"] = e["product_name_fr"]
            #aliments["categories"] = e["categories"]
            aliments["categories"] = [e_1.replace("en:", "") for e_1 in e["categories_hierarchy"]]
            aliments["brand"] = e["brands"].replace(",",", ")
            aliments["purchase_place"] = e["purchase_places"].replace(",",", ")
            aliments["store"] = e["stores"].replace(",",", ")
            aliments["images"] = e["selected_images"]
            data["rcvd"]["essentials"]["aliments"][i] = aliments
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

    #session = Data("biscuit")
    #result = session.big_data
    #print("fin d'operation")
    ##print("\n")

    session = DataEngine("biscuit")
    result = session.big_data
    print("ok")
