from django import forms
from .models import Address, Region, City


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['region', 'city']
