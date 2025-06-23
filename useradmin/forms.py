from django import forms
from core.models import Product, Category, Supplier, Brand, Flavor

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'old_price', 'quantity', 'category', 'image', 'supplier', 'brand', 'flavors', 'in_stock']
        widgets = {      
            'title': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter product title'}),
            'description': forms.Textarea(attrs={'class': 'form', 'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'class': 'form', 'placeholder': 'Enter product price'}),
            'old_price': forms.NumberInput(attrs={'class': 'form', 'placeholder': 'Enter old price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form', 'placeholder': 'Enter quantity'}),
            'category': forms.Select(attrs={'class': 'form bg-[#414141]'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form'}),
            'supplier': forms.Select(attrs={'class': 'form bg-[#414141]'}),
            'brand': forms.Select(attrs={'class': 'form bg-[#414141]'}),
            'flavors': forms.SelectMultiple(attrs={'class': 'form'}),
            'in_stock': forms.CheckboxInput(attrs={'class': 'form'})
        }

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter category title'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form'})
        }