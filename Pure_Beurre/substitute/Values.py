""""""
# -*- coding: utf-8 -*-
from .models import Aliment as AlimentDB, Category as CategoryDB


class AlimentValue:
    """"""
    def __init__(self, brand, product_name, category, nutriscore, purchase_place, store, url):
        print("\n**** creation aliment en cours ****\n")
        self.brand = brand
        self.product_name = product_name
        self.category = category
        self.nutriscore = nutriscore
        self.purchase_place = purchase_place
        self.store = store
        self.url = url

    def store_items(self):
        an_aliment = AlimentDB()
        an_aliment.brand = self.brand
        an_aliment.name = self.product_name
        an_aliment.purchase_places = self.purchase_place
        an_aliment.nutriscore = self.nutriscore
        an_aliment.store = self.store
        an_aliment.url = self.url
        #an_aliment = AlimentDB(
        #    brand=self.brand,
        #    name=self.product_name,
        #    category=self.category,
        #    nutriscore=self.nutriscore,
        #    purchase_places=self.purchase_place,
        #    store=self.store,
        #    url=self.url
        #)
        print("\n**** aliment cree ****\n")
        an_aliment.save()
        #an_aliment.category.add(self.category)


class CategoryValue:
    """"""

    def __init__(self, id_name, name, url):
        print("\n**** creation aliment en cours ****\n")
        self.id_name = id_name
        self.name = name
        self.url = url

    def store_items(self):
        a_category = CategoryDB(
            id_name=self.id_name,
            name=self.name,
            url=self.url
        )
        print("\n**** categorie cree ****\n")
        a_category.save()

if __name__ == "__main__":

    pass
