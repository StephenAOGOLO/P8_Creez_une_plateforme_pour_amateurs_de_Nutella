""" This module is listing all the models which are needed for the application Web Site 'substitute'. """
from django.db import models
from django.contrib.auth.models import User
# -*- coding: utf-8 -*-

# Create your models here.

class Text(models.Model):
    """ This model is used for displaying text into two templates :
        home.html and mentions.html."""
    language = models.CharField(max_length=2, null=True)
    mentions_title = models.CharField(max_length=1000, null=True)
    mentions_id_fn = models.CharField(max_length=1000, null=True)
    mentions_id_ln = models.CharField(max_length=1000, null=True)
    mentions_id_ph = models.CharField(max_length=1000, null=True)
    mentions_id_m = models.CharField(max_length=1000, null=True)
    mentions_id_pn = models.CharField(max_length=1000, null=True)
    mentions_id_s = models.CharField(max_length=1000, null=True)
    mentions_a_rcs = models.CharField(max_length=1000, null=True)
    mentions_a_fn = models.CharField(max_length=1000, null=True)
    mentions_a_cgv = models.CharField(max_length=1000, null=True)
    mentions_cookies = models.CharField(max_length=1000, null=True)
    home_s = models.CharField(max_length=1000, null=True)
    home_c = models.CharField(max_length=1000, null=True)
    home_bm = models.CharField(max_length=1000, null=True)


class Customer(models.Model):
    """ This model is a special user model. It is especially used for identify a record's owner """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        """ This method displaying the user's name when a customer model instance is called. """
        return self.user.username


class Category(models.Model):
    """ This model's describing a product's category.
    It is linked to Aliment model by a 'many to many relationship'."""
    id_name = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)

    def __str__(self):
        """ This method displaying the category's name when the model instance is called. """
        return self.name


class Aliment(models.Model):
    """ This model's describing a product.
    It is linked to Category model by a 'many to many relationship'."""
    name = models.CharField(max_length=500, null=True)
    tag = models.ManyToManyField(Category)
    category = models.CharField(max_length=500, null=True)
    brand = models.CharField(max_length=500, null=True)
    nutriscore = models.CharField(max_length=1, null=True)
    image_nutriments = models.URLField(max_length=500, null=True)
    energy_kj = models.CharField(max_length=100, null=True)
    energy_kj_unit = models.CharField(max_length=100, null=True)
    energy_kcal = models.CharField(max_length=100, null=True)
    energy_kcal_unit = models.CharField(max_length=100, null=True)
    store = models.CharField(max_length=500, null=True)
    purchase_places = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)
    url_image = models.URLField(max_length=500, null=True)

    def __str__(self):
        """ This method displaying the product's name when the model instance is called. """
        return self.name


class Historic(models.Model):
    """ This model's describing a historic record.
    A record is composed of its owner, a product and its substitute."""
    user = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, related_name="aliment", null=True, on_delete=models.CASCADE)
    substitute = models.ForeignKey(Aliment,related_name="substitute", null=True, on_delete=models.CASCADE)

    def __str__(self):
        """ This method displaying the record's id when the model instance is called. """
        return str(self.id)
