from django.urls import path
from useradmin import views

app_name = 'useradmin'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.admin_products_view, name='products'),
    path('add-product/', views.add_product_view, name='add-product'),
    path('edit-product/<pid>/', views.edit_product_view, name='edit-product'),
    path('delete-product/<pid>/', views.delete_product_view, name='delete-product'),
    path('orders/', views.admin_orders_view, name='orders'),
    path('order-detail/<oid>/', views.order_detail_view, name='order-detail'),
    path('order-status/<oid>/', views.change_order_status, name='order-status'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('category/', views.admin_categories_view, name='category'),
    path('add-category/', views.add_category_view, name='add-category'),
    path('edit-category/<cid>/', views.edit_category_view, name='edit-category'),
    path('delete-category/<cid>/', views.delete_category_view, name='delete-category'),
    path('brand/', views.admin_brands_view, name='brand'),
    path('add-brand/', views.add_brand_view, name='add-brand'),
    path('edit-brand/<bid>/', views.edit_brand_view, name='edit-brand'),
    path('delete-brand/<bid>/', views.delete_brand_view, name='delete-brand'),
    path('flavor/', views.admin_flavors_view, name='flavor'),
    path('add-flavor/', views.add_flavor_view, name='add-flavor'),
    path('edit-flavor/<id>/', views.edit_flavor_view, name='edit-flavor'),
    path('delete-flavor/<id>/', views.delete_flavor_view, name='delete-flavor'),
    path('change-password/', views.admin_change_password, name='change-password'),
]