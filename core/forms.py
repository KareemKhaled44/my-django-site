from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name',
                  'phone', 'email', 'street_address', 'apartment', 'city', 'postal_code']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form', 'placeholder': 'First name', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Last name', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Phone', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form', 'placeholder': 'Email', 'required': 'required'}),
            'street_address': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Street Address', 'required': 'required'}),
            'apartment': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Apartment / Unit (optional)'}),
            'postal_code': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Postal Code', 'required': 'required'}),
            'city': forms.Select(attrs={'class': 'select-form', 'required': 'required'}),
        }