""" This module allowing to include an application to the project.
 It's helping to configure some of the attributes of the application.  """
from django.apps import AppConfig


class SubstituteConfig(AppConfig):
    """ The application 'substitute' and its configuration are added. """
    name = 'substitute'
