""" This module is Django’s command-line utility for administrative tasks. """
from django.contrib import admin

# Register your models here.

from .models import *
""" This section enable models which are displayed on admin console. """
admin.site.register(Customer)
admin.site.register(Aliment)
admin.site.register(Category)
admin.site.register(Historic)
