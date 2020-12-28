""" This module using the 'User' model and UserCreationForm format  to create new users """
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    """ This class inherits from UserCreationForm.
      However, its behaviour is based on models.User.
      So, the authentification is handled by Django."""
    class Meta:
        """ This class provides User model and edits username,
         email passwords."""
        model = User
        fields = ["username", "email", "password1", "password2"]
