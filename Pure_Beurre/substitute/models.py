from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    id_name = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)

    def __str__(self):
        return self.name


class Aliment(models.Model):
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
        return self.name


class Historic(models.Model):
    user = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, related_name="aliment", null=True, on_delete=models.CASCADE)
    substitute = models.ForeignKey(Aliment,related_name="substitute", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)



