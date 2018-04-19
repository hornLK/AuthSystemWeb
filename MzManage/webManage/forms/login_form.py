from django.forms import CharField, EmailField,BooleanField
from django import forms
from django.forms.widgets import PasswordInput,CheckboxInput, EmailInput

class LoginForm(forms.Form):
    email = EmailField( widget= EmailInput(attrs={
        'class': 'form-control','placeholder':'Email','type':'email'
                            }), required=True)

    password = CharField(max_length=200, widget=PasswordInput(attrs={
        'class': 'form-control','placeholder':'Password','type':'password'
                            }), required=True)
    remember = BooleanField(widget=CheckboxInput(attrs={'type':'checkbox'}),
                           required=False)

