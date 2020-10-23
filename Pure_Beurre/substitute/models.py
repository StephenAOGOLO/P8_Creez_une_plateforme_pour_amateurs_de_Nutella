from django.db import models

# Create your models here.

class Users(models.Model):
    col = models.CharField(max_length=50)