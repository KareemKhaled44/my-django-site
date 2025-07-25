from django.db import models
from shortuuidfield import ShortUUIDField
import shortuuid
from django.utils.html import mark_safe 
from userauths.models import User
from decimal import Decimal


STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('deleted', 'Deleted'),
)

ORDER_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
)

PAYMENT_METHOD_CHOICES = [
    ('Cash on Delivery', 'Cash on Delivery'),
    ('Vodafone Cash', 'Vodafone Cash'),
]

CITIES = [
    ("Cairo", "Cairo"),
    ("Alexandria", "Alexandria"),
    ("Giza", "Giza"),
    ("Mansoura", "Mansoura"),
    ("Tanta", "Tanta"),
    ("Aswan", "Aswan"),
    ("Assiut", "Assiut"),
    ("Zagazig", "Zagazig"),
    ("Ismailia", "Ismailia"),
    ("Fayoum", "Fayoum"),
]

# Create your models here.
class Category(models.Model):
      cid= ShortUUIDField(primary_key=True)
      title=models.CharField(max_length=100)
      image=models.ImageField(upload_to='category')

      class Meta:
          verbose_name = "Category"
          verbose_name_plural = "Categories"

      def save(self, *args, **kwargs):
        if not self.cid:
            self.cid = shortuuid.ShortUUID().random(length=8).upper()
            prefix = "CAT-"
            self.cid = f"{prefix}{self.cid}"
        super().save(*args, **kwargs) 

      #function to show image in admin panel
      def category_image(self):
            if self.image:
                return mark_safe(f'<img src="{self.image.url}" height="70" width="70" />')
            return "No Image"
      
      def __str__(self):
        return self.title

class Supplier(models.Model):
    sid= ShortUUIDField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(blank=True, null=True)
    phone=models.CharField(max_length=15, blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #to show user who created the supplier
    days_return = models.PositiveIntegerField(default=0)  # number of days for return policy
    authentic_rating = models.IntegerField(default=5) # to show rating of the supplier
    class Meta:
        verbose_name_plural='suppliers' #to show plural name in admin panel

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.sid:
            self.sid = shortuuid.ShortUUID().random(length=8).upper()
            prefix = "SUP-"
            self.sid = f"{prefix}{self.sid}"
        super().save(*args, **kwargs)
    

############################ flavor model ###############################
class Flavor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name if self.name else "No Flavor"
    
############################ brand model ###############################
class Brand(models.Model):
    bid= ShortUUIDField(primary_key=True)
    name=models.CharField(max_length=100, blank=False, null=False)
    image=models.ImageField(upload_to='brand', blank=True, null=True) #to show image of the brand
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #to show user who created the brand
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='brands'

    def brand_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="70" width="70" />')
        return "No Image"

    def __str__(self):
        return self.name if self.name else "Unnamed Brand"
    
class Product(models.Model):
    pid= ShortUUIDField(primary_key=True)
    title=models.CharField(max_length=100, blank=False, null=False)
    image=models.ImageField(upload_to='product')
    description=models.TextField(blank=True, null=True, default='this is a product')

    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    old_price=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    specifications=models.TextField(blank=True, null=True)

    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #to show user who created the product
    category=models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category') #to show category of the product
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True) #to show supplier of the product
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)

    is_active=models.BooleanField(default=True) #to show if the product is active or not
    product_status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='active') 
    in_stock=models.BooleanField(default=True) #to show if the product is in stock or not
    
    quantity=models.PositiveIntegerField(default=0) 
    quantity_sold=models.PositiveIntegerField(default=0)
    featured=models.BooleanField(default=False) #عشان العروض
    sku=models.CharField(max_length=100,unique=True, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    flavors = models.ManyToManyField(Flavor, blank=True)

    
    
    class Meta:
        verbose_name_plural='products'

    def save(self, *args, **kwargs):
        # First part: Check and generate SKU and pid if not exists
        if not self.pid:
            self.pid = shortuuid.ShortUUID().random(length=8).upper()
            prefix="PROD-"
            self.pid = f"{prefix}{self.pid}"

        
        
        if not self.sku:
            prefix = "PROD-"  
            random_code = shortuuid.ShortUUID().random(length=8).upper()
            self.sku = f"{prefix}{random_code}"

         #Second part: Update in_stock based on quantity
        self.in_stock = self.quantity > 0

        # Call the original save method
        super().save(*args, **kwargs)
    
    def product_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="70" width="70" />')
        return "No Image"
    
    #function to show the discount percentage
    def get_discount_percentage(self):
      if self.old_price and self.old_price > 0 and self.price < self.old_price:
          discount = 100 - ((self.price / self.old_price) * 100)
          return round(discount, 1)
      return 0 #if no discount

    
    def __str__(self):
        return self.title if self.title else "Unnamed Product"

    
class ProductImages(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='internal_images') #to show product of the image
    image=models.ImageField(upload_to='product_images') #to show image of the product
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title if self.product else "No Product"
    
############################# wishlist model ###############################
class Wishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True) #to show product of the wishlist
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural='wishlists' #to show plural name in admin panel
    def __str__(self):
        return f"{self.user.username} - {self.product.title}" if self.user and self.product else "Wishlist Item"

############################# address model ###############################
class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #to show user who created the address
    first_name=models.CharField(max_length=100, blank=True, null=True)
    last_name=models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)  # Email field for the address
    phone=models.CharField(max_length=20, blank=True, null=True)

    street_address = models.CharField(max_length=255, blank=True, null=True)
    apartment = models.CharField(max_length=50, blank=True, null=True) 

    status=models.BooleanField(default=False) #to show if the address is default or not

    postal_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, choices=CITIES, default='Cairo', blank=True, null=True)  # Default city is Cairo

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='addresses'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.street_address}, {self.city}" if self.first_name and self.last_name else "Unnamed Address"


############################# coupon model ###############################
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='coupons'

    def __str__(self):
        return self.code

############################ cartorder, cartorderitem models ###############################
class CartOrder(models.Model):
    oid = ShortUUIDField(primary_key=True)
    invoice_number=ShortUUIDField(max_length=100, blank=True, null=True) #to show invoice number of the item

    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #to show user who created the cart order
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    coupons = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #to show saved amount of the order
    total_price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #to show total price of the order
    order_date=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='pending')
    paid_status=models.BooleanField(default=False) #to show if the order is paid or not

    shipping_cost=models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #to show shipping price of the item
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)


    class Meta:
        verbose_name_plural='cart orders'


    

    def save(self, *args, **kwargs):
        if not self.oid:
            self.oid = shortuuid.ShortUUID().random(length=8).upper()
            prefix = "ORD-"
            self.oid = f"{prefix}{self.oid}"
        if not self.invoice_number:
            self.invoice_number = shortuuid.ShortUUID().random(length=8).upper()
            prefix = "INV-"
            self.invoice_number = f"{prefix}{self.invoice_number}"
        super().save(*args, **kwargs) 


    def __str__(self):
        return f"Order {self.pk} - {self.user.username if self.user else 'Guest'}"

class CartOrderItem(models.Model):
    order=models.ForeignKey(CartOrder, on_delete=models.CASCADE, null=True, blank=True) #to show cart order of the item
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True) #to show product of the item
    image=models.ImageField(max_length=100, blank=True, null=True) #to show image of the item
    quantity=models.PositiveIntegerField(default=1) 
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    total_price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural='cart order items'
    
    def order_image(self):
        if self.product and self.product.image:
            return mark_safe(f'<img src="{self.product.image.url}" height="70" width="70" />')
        return "No Image"
    
    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
    


