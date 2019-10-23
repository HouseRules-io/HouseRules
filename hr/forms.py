from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import House, Rulebook, Rule

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Please enter your first name.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Please enter your last name.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class HouseForm(ModelForm):
    class Meta:
        model = House
        fields = ['house_name']

class RulebookForm(ModelForm):
    class Meta:
        model = Rulebook
        fields = ['rulebook_name']

class RuleForm(ModelForm):
    class Meta:
        model = Rule
        fields = ['rule_name', 'rule_text']