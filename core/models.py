from django.db import models
from shortuuidfield import ShortUUIDField
import shortuuid
from django.utils.html import mark_safe 
from userauths.models import User


STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('deleted', 'Deleted'),
)

ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('canceled', 'Canceled'),
)



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
                return mark_safe(f'<img src="{self.image.url}" height="50" width="50" />')
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
    days_return = models.PositiveIntegerField(default=0)  # عدد الأيام اللي ممكن يرجّع فيها
    authentic_rating = models.IntegerField(default=5) # تقييم المورد

    class Meta:
        verbose_name_plural='suppliers' #to show plural name in admin panel

    def __str__(self):
        return self.name
    

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
            return mark_safe(f'<img src="{self.image.url}" height="30" width="30" />')
        return "No Image"

    def __str__(self):
        return self.name if self.name else "Unnamed Brand"
    
class Product(models.Model):
    pid= ShortUUIDField(primary_key=True)
    title=models.CharField(max_length=100, blank=False, null=False)
    image=models.ImageField(upload_to='product')
    description=models.TextField(blank=True, null=True, default='this is a product')
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
            return mark_safe(f'<img src="{self.image.url}" height="50" width="50" />')
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



############################ cart, order, orderitem models ###############################
class CartOrder(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #to show user who created the cart order
    total_price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    order_date=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='pending')
    paid_status=models.BooleanField(default=False) #to show if the order is paid or not
    shipping_price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #to show shipping price of the item

    class Meta:
        verbose_name_plural='cart orders'

    def update_total_price(self):
        total = self.cartorderitem_set.aggregate(total=models.Sum('total_price'))['total'] or 0
        self.total_price = total
        self.save()


    def __str__(self):
        return f"Order {self.pk} - {self.user.username if self.user else 'Guest'}"

class CartOrderItem(models.Model):
    order=models.ForeignKey(CartOrder, on_delete=models.CASCADE, null=True, blank=True) #to show cart order of the item
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True) #to show product of the item
    image=models.CharField(max_length=100, blank=True, null=True) #to show image of the item
    quantity=models.PositiveIntegerField(default=1) 
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    total_price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_number=models.CharField(max_length=100, blank=True, null=True) #to show invoice number of the item
    
    class Meta:
        verbose_name_plural='cart order items'
    
    def save(self, *args, **kwargs):
        # Calculate the total price of the item
        self.total_price = self.quantity * self.price
        
        # Save the cart order item
        super().save(*args, **kwargs)
        
        # After saving, update the total price of the order
        if self.order:
            self.order.update_total_price()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        
        # After deleting, update the total price of the order
        if order:
            order.update_total_price()


    def order_image(self):
        if self.product and self.product.image:
            return mark_safe(f'<img src="{self.product.image.url}" height="50" width="50" />') 
        return "No Image"
    
    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
    
############################# address model ###############################
class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #to show user who created the address
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=15, blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    status=models.BooleanField(default=False) #to show if the address is default or not
    city=models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural='addresses'

    