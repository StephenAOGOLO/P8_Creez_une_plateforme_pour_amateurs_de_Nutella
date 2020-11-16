from django.db import models

# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


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
    store = models.CharField(max_length=500, null=True)
    purchase_places = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)

    def __str__(self):
        return self.name


class Historic(models.Model):
    user = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, related_name="aliment", null=True, on_delete=models.CASCADE)
    substitute = models.ForeignKey(Aliment,related_name="substitute", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



