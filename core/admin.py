from django.contrib import admin
from core.models import Product, ProductImages, Coupon, Category, Address, Supplier, CartOrder, CartOrderItem, Flavor, Brand
# Register your models here.
class ProductImages(admin.TabularInline):
      model = ProductImages
      extra = 1


class FlavorAdmin(admin.ModelAdmin):
    list_display = ['name']

class BrandAdmin(admin.ModelAdmin):
      list_display = ('bid', 'name', 'brand_image')

class ProductAdmin(admin.ModelAdmin):
      list_display = ('sku','pid','title', 'price', 'product_image', 'category', 'user', 'product_status')
      list_filter = ('category', 'product_status')
      filter_horizontal = ('flavors',)
      readonly_fields = ('sku', 'pid')
      inlines = [ProductImages]

class CategoryAdmin(admin.ModelAdmin):
      list_display = ('cid', 'title', 'category_image')
      

class CartOrderAdmin(admin.ModelAdmin):
      list_display = ('oid','user', 'order_status', 'paid_status', 'order_date', 'price', 'saved', 'total_price')
      list_filter = ('order_status', 'paid_status')
      search_fields = ('user', 'order_date')

class CartOrderItemAdmin(admin.ModelAdmin):
      list_display = ('order', 'product', 'order_image', 'quantity', 'price', 'total_price', 'invoice_number')
      list_filter = ('order', 'product')

class AddressAdmin(admin.ModelAdmin):
      list_display = ('first_name', 'last_name','city')
      search_fields = ('first_name', 'last_name', 'city', 'postal_code')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Supplier)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
admin.site.register(Flavor, FlavorAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Coupon)

