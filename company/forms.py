from django import forms
from user.models import Address
from .models import CompanyProfile


class VenueProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'address', 'capacity', 'venue_type']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['region', 'city']


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'address', 'capacity', 'venue_type', 'image', 'video', 'panorama']
        widgets = {
            'venue_type': forms.Select(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['address'].queryset = Address.objects.all()
