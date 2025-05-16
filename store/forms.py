# store/forms.py

from django import forms
from .models import Phone
from .models import Customer

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['name', 'brand', 'price', 'description', 'image']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_bought']

class UpdateStockForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['stock']  # Only the stock field