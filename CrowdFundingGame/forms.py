from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class SignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    password_repeat = forms.CharField(label="Re-enter Password", max_length=30,
                                      widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password2'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already used choose other")
        return username

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['password_repeat']:
            self._errors["password"] = ["Password do not match"]  # Will raise a error message
            del form_data['password']
        return form_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('college', 'contact', 'type')
        widgets = {'contact': PhoneNumberPrefixWidget(attrs={'id':'mySelect', 'placeholder': 'Phone number'})}


class TransactionForm(forms.Form):  # error
    send_to = forms.ModelChoiceField(User.objects.filter(profile__type__exact=1))
    money = forms.IntegerField(label="Money",
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'name': 'money'}))

    def valid_transaction(self):
        money = self.cleaned_data['money']
        if money < 0:
            self._errors["money"] = ["Invalid Amount"]  # Will raise a error message