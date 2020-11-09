from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name


class Aliment(models.Model):
    name = models.CharField(max_length=500, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Historic(models.Model):
    user = models.ForeignKey(Users, null=True, on_delete=models.SET_NULL)
    aliment = models.ForeignKey(Aliment, null=True, on_delete=models.SET_NULL)
