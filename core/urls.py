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
]