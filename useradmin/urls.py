from django.urls import path
from useradmin import views

app_name = 'useradmin'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.admin_products_view, name='products'),
    path('add-product/', views.add_product_view, name='add-product'),
    path('edit-product/<pid>/', views.edit_product_view, name='edit-product'),
    path('delete-product/<pid>/', views.delete_product_view, name='delete-product'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('category/', views.admin_categories_view, name='category'),
    path('add-category/', views.add_category_view, name='add-category'),

    path('delete-category/<cid>/', views.delete_category_view, name='delete-category'),

]