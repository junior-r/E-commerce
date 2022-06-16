from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Coupon


class DateInput(forms.DateInput):
    input_type = 'date'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'JohnDoe25'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'John@example.com'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'first_name': None,
            'last_name': None,
            'username': None,
            'email': None,
        }


class CouponForm(forms.Form):
    discount = forms.DecimalField(max_digits=4, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class': 'form-control my-3'}), label='Descuento')
    valid_from = forms.DateField(widget=DateInput(attrs={'class': 'form-control my-3', 'type': 'date'}), required=True, label='Fecha de inicio')
    valid_to = forms.DateField(widget=DateInput(attrs={'class': 'form-control my-3', 'type': 'date'}), required=True, label='Fecha de fin')
    active = forms.BooleanField(required=True, label='¿Activo?', widget=forms.CheckboxInput(attrs={'class': 'form-checkbox my-3'}))

    class Meta:
        model = Coupon
        fields = ['discount', 'valid_from', 'valid_to', 'active']

    def clean_valid_from(self):
        valid_from = self.cleaned_data.get('valid_from')
        if valid_from < datetime.date(datetime.now()):
            raise forms.ValidationError('La fecha de inicio debe ser posterior a la actual.')
        return valid_from

    def clean_valid_to(self):
        valid_to = self.cleaned_data.get('valid_to')
        if valid_to < datetime.date(datetime.now()):
            raise forms.ValidationError('La fecha de fin debe ser posterior a la actual.')
        return valid_to

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount < 0 or discount > 100:
            raise forms.ValidationError('El descuento debe estar entre 0 y 100.')
        return discount

