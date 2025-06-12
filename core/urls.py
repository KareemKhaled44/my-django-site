from django.urls import path
from . import views

app_name = 'core'


urlpatterns = [
      path('', views.index, name='index'),
      path('products/<str:cid>/', views.product_list_view, name='category-product-list'),
      path('products/', views.product_list_view, name='product-list'),
      path('product/<str:pid>/', views.product_detail, name='product-detail'),
      path('search/', views.product_list_view, name='search'),
      path('api/search-products/', views.search_products, name='api-search-products'),
      path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
      path('cart/', views.cart_view, name='cart'),
      path('delete-from-cart/', views.delete_cart_item, name='delete-from-cart'),
      path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
      path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
      path('checkout/', views.checkout_view, name='checkout'),
      path('invoice/', views.invoice_view, name='invoice'),
      path('contact_us/', views.contact_view, name='contact_us'),
      path('Ajax_contact_form/', views.Ajax_contact_form, name='Ajax_contact_form'),
]