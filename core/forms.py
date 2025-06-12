from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name',
                  'phone', 'email', 'street_address', 'apartment', 'city', 'postal_code']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-[#414141] bg-transparent text-[#F9FAFB] text-sm rounded-md focus:border-[#b9a848] outline-0', 'placeholder': 'First name', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-[#414141] bg-transparent text-[#F9FAFB] text-sm rounded-md focus:border-[#b9a848] outline-0', 'placeholder': 'Last name', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-[#414141] bg-transparent text-[#F9FAFB] text-sm rounded-md focus:border-[#b9a848] outline-0', 'placeholder': 'Phone', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 border border-[#414141] bg-transparent text-[#F9FAFB] text-sm rounded-md focus:border-[#b9a848] outline-0', 'placeholder': 'Email', 'required': 'required'}),
            'street_address': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-[#414141] bg-transparent text-[#F9FAFB] text-sm rounded-md focus:border-[#b9a848] outline-0', 'placeholder': 'Street Address', 'required': 'required'}),
            'apartment': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-[#414141] bg-transparent text-[#F9FAFB] text-sm rounded-md focus:border-[#b9a848] outline-0', 'placeholder': 'Apartment / Unit (optional)'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-[#414141] bg-transparent text-[#F9FAFB] text-sm rounded-md focus:border-[#b9a848] outline-0', 'placeholder': 'Postal Code', 'required': 'required'}),
            'city': forms.Select(attrs={'class': 'w-full px-4 py-3  bg-[#414141] text-[#F9FAFB] text-sm rounded-md focus:border-[#b9a848] outline-0'}),
        }