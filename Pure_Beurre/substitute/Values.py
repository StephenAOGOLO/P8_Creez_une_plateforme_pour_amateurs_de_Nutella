""""""
# -*- coding: utf-8 -*-
import logging as lg
from .models import Aliment as AlimentDB, Category as CategoryDB, Historic as HistoricDB, Text as TextDB
lg.basicConfig(level=lg.INFO)


class TextValue:
    def __init__(self, data):
        self.values = data
        self.set_text()

    def set_text(self):
        the_text = TextDB()
        the_text.language = self.values["language"]
        the_text.mentions_title = self.values["m_t"]
        the_text.mentions_id_fn = self.values["m_id_fn"]
        the_text.mentions_id_ln = self.values["m_id_ln"]
        the_text. mentions_id_ph = self.values["m_id_ph"]
        the_text.mentions_id_m = self.values["m_id_m"]
        the_text.mentions_id_pn = self.values["m_id_pn"]
        the_text.mentions_id_s = self.values["m_id_s"]
        the_text.mentions_a_rcs = self.values["m_a_rcs"]
        the_text.mentions_a_fn = self.values["m_a_fn"]
        the_text.mentions_a_cgv = self.values["m_a_cgv"]
        the_text.mentions_cookies = self.values["m_c"]
        the_text.home_s = self.values["h_s"]
        the_text.home_c = self.values["h_c"]
        the_text.home_bm = self.values["h_bm"]
        the_text.save()
        #(
        #    language = self.values
        #    self.m_t =
        #    self.m_id_fn =
        #    self.m_id_ln =
        #    self.m_id_ph =
        #    self.m_id_m =
        #    self.m_id_ph =
        #    self.m_id_s =
        #    self.m_a_rcs =
        #    self.m_a_fn =
        #    self.m_a_cgv =
        #    self.m_c =
        #    self.h_s =
        #    self.h_c =
        #    self.h_bm =
        #)

    #def store_data(self):
    #    the_text = TextDB()
    #    the_text.language = self.language
    #    the_text.footer = self.footer
    #    the_text.home = self.home
    #    the_text.save()

class AlimentValue:
    """"""
    def __init__(self, brand, product_name, category, nutriscore, purchase_place, store, url, url_image, energy_img, energy_kj, energy_kcal, energy_kj_unit, energy_kcal_unit):
        self.brand = brand
        self.product_name = product_name
        self.category = category
        self.nutriscore = nutriscore
        self.purchase_place = purchase_place
        self.store = store
        self.url = url
        self.url_image = url_image
        self.energy_img = energy_img
        self.energy_kj = energy_kj
        self.energy_kj_unit = energy_kj_unit
        self.energy_kcal = energy_kcal
        self.energy_kcal_unit = energy_kcal_unit

    def store_items(self):

        an_aliment = AlimentDB()
        an_aliment.brand = self.brand
        an_aliment.name = self.product_name
        an_aliment.purchase_places = self.purchase_place
        an_aliment.nutriscore = self.nutriscore
        an_aliment.store = self.store
        an_aliment.url = self.url
        an_aliment.url_image = self.url_image

        an_aliment.image_nutriments = self.energy_img
        an_aliment.energy_kcal = self.energy_kcal
        an_aliment.energy_kcal_unit = self.energy_kcal_unit
        an_aliment.energy_kj = self.energy_kj
        an_aliment.energy_kj_unit = self.energy_kj_unit

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


class HistoricValue:
    def __init__(self, aliment, substitute, customer):
        self.aliment = aliment
        self.substitute = substitute
        self.customer = customer

    def store_items(self):
        a_historic = HistoricDB(
            user=self.customer,
            aliment=self.aliment,
            substitute=self.substitute
        )
        a_historic.save()
        print("Enregistrement ajouté à l'historique :\n{}\n".format(a_historic.id))
