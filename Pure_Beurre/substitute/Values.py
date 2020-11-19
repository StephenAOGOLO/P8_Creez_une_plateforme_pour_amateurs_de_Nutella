""""""
# -*- coding: utf-8 -*-
import logging as lg
from .models import Aliment as AlimentDB, Category as CategoryDB
lg.basicConfig(level=lg.INFO)


class AlimentValue:
    """"""
    def __init__(self, brand, product_name, category, nutriscore, purchase_place, store, url, url_image):
        self.brand = brand
        self.product_name = product_name
        self.category = category
        self.nutriscore = nutriscore
        self.purchase_place = purchase_place
        self.store = store
        self.url = url
        self.url_image = url_image

    def store_items(self):

        an_aliment = AlimentDB()
        an_aliment.brand = self.brand
        an_aliment.name = self.product_name
        an_aliment.purchase_places = self.purchase_place
        an_aliment.nutriscore = self.nutriscore
        an_aliment.store = self.store
        an_aliment.url = self.url
        an_aliment.url_image = self.url_image
        str_cat = ""
        for e in self.category:
            str_cat = str_cat+" "+e
        an_aliment.category = str_cat
        an_aliment.save()
        print("Enregistrement de l'aliment :\n{}\n".format(an_aliment))
        for i, e in enumerate(self.category):
            try:
                if CategoryDB.objects.get(id_name=e):
                    his_category = CategoryDB.objects.get(id_name=e)
                    an_aliment.tag.add(his_category)
            except Exception as e:
                lg.debug(e)



class CategoryValue:
    """"""

    def __init__(self, id_name, name, url):
        self.id_name = id_name
        self.name = name
        self.url = url

    def store_items(self):
        a_category = CategoryDB(
            id_name=self.id_name,
            name=self.name,
            url=self.url
        )
        a_category.save()
        print("Enregistrement de la catégorie :\n{}\n".format(a_category))

