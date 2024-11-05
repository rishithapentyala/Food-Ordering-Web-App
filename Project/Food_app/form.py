from django.contrib.auth.forms import UserCreationForm
from .models import User # this 'User' is considered as a model, we already imported in models.py file
from django import forms

# creating of custom user registration form

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2'] # this is the procedure of creating 'fields' name ['username','email','password1','password2'], we can't give any other names in 'fields'
