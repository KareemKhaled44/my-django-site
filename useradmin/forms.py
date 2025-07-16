from django import forms
from core.models import Product, CartOrder, CartOrderItem, Category, Supplier, Brand, Flavor, Address, Coupon

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

class AddCartOrderForm(forms.ModelForm):
    class Meta:
        model = CartOrder
        fields = ['user', 'address', 'coupons',  'payment_method', 'order_status', 'paid_status']
        widgets = {
            'user': forms.Select(attrs={'class': ' searchable'}),
            'address': forms.Select(attrs={'class': 'form bg-[#414141]'}),
            'coupons': forms.SelectMultiple(attrs={'class': 'form bg-[#414141]'}),
            'payment_method': forms.Select(attrs={'class': 'form bg-[#414141]'}),
            'order_status': forms.Select(attrs={'class': 'form bg-[#414141]'}),
            'paid_status': forms.CheckboxInput(attrs={'class': 'form'}),
        }

class AddOrderItemForm(forms.ModelForm):
    class Meta:
        model = CartOrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'searchable bg-[#414141]'}),
            'quantity': forms.NumberInput(attrs={'class': 'form'}),
        }
    #get only in stock products
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(in_stock=True)

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter category title'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form'})
        }

class AddBrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'image', 'user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter brand title'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form'}),
            'user': forms.Select(attrs={'class': 'form bg-[#414141]'})
        }

class AddFlavorForm(forms.ModelForm):
    class Meta:
        model = Flavor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter flavor name'}),
        }

class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'email', 'street_address', 'apartment', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter last name'}),
            'phone': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form', 'placeholder': 'Enter email address'}),
            'street_address': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter street address'}),
            'apartment': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter apartment number (optional)'}),
            'postal_code': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter postal code'}),
            'city': forms.Select(attrs={'class': 'form bg-[#414141]'}),
        }

class AddCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage', 'active']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter coupon code'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form', 'placeholder': 'Enter discount percentage'}),
            'active': forms.CheckboxInput(attrs={'class': 'form'})
        }

class AddSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'email', 'user', 'address', 'days_return', 'authentic_rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter supplier name'}),
            'phone': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter contact information'}),
            'email': forms.EmailInput(attrs={'class': 'form', 'placeholder': 'Enter supplier email'}),
            'user': forms.Select(attrs={'class': 'searchable'}),
            'address': forms.Textarea(attrs={'class': 'form', 'placeholder': 'Enter supplier address'}),
            'days_return': forms.NumberInput(attrs={'class': 'form', 'placeholder': 'Enter days for return policy'}),
            'authentic_rating': forms.NumberInput(attrs={'class': 'form', 'placeholder': 'Enter authentic rating (1-5)'}),
        }