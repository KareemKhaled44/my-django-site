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
      path('update-cart-preview/', views.update_cart_preview, name='update-cart-preview'),
      path('cart/', views.cart_view, name='cart'),
      path('delete-from-cart/', views.delete_cart_item, name='delete-from-cart'),
      path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
      path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
      path('checkout/', views.checkout_view, name='checkout'),
      path('vodafone-instructions/', views.voda_payment_instructions_view, name='vodafone-instructions'),
      path('invoice/', views.invoice_view, name='invoice'),
      path('contact_us/', views.contact_view, name='contact_us'),
      path('Ajax_contact_form/', views.Ajax_contact_form, name='Ajax_contact_form'),
      path('dashboard/', views.customer_dashboard, name='dashboard'),
      path('dashboard/orders/<str:oid>/', views.order_detail, name='order-detail'),
      path('make-default-address/', views.make_default_address, name='make-default-address'),
      path('delete-address/', views.delete_address, name='delete-address'),
      path('dashboard/edit-address/<int:id>/', views.edit_address, name='edit-address'),
      path('dashboard/add-address/', views.add_address, name='add-address'),
      path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
      path('delete_from_wishlist/', views.delete_from_wishlist, name='delete_from_wishlist'),
      path('about-us/', views.about_us, name='about-us'),
      path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
      path('shipping-policy/', views.shipping_policy, name='shipping-policy'),
      path('return-policy/', views.return_policy, name='return-policy'),

]