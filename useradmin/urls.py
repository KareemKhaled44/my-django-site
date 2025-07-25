from django.urls import path
from useradmin import views

app_name = 'useradmin'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.admin_products_view, name='products'),
    path('add-product/', views.add_product_view, name='add-product'),
    path('edit-product/<pid>/', views.edit_product_view, name='edit-product'),
    path('delete-internal-image/<int:img_id>/', views.delete_internal_image, name='delete-internal-image'),
    path('delete-product/<pid>/', views.delete_product_view, name='delete-product'),
    path('orders/', views.admin_orders_view, name='orders'),
    path('order-detail/<oid>/', views.order_detail_view, name='order-detail'),
    path('order-status/<oid>/', views.change_order_status, name='order-status'),
    path('order-paid-status/<oid>/', views.change_order_paid_status, name='order-paid-status'),
    path('add-order/', views.add_order_view, name='add-order'),
    path('add-order-items/<oid>/', views.add_order_items_view, name='add-order-items'),
    path('delete-order-item/<oid>/<item_id>/', views.delete_order_item_view, name='delete-order-item'),
    path('delete-order/<oid>/', views.delete_order_view, name='delete-order'),
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
    path('addresses/', views.admin_addresses_view, name='addresses'),
    path('add-address/', views.add_address_view, name='add-address'),
    path('edit-address/<id>/', views.edit_address_view, name='edit-address'),
    path('delete-address/<id>/', views.delete_address_view, name='delete-address'),
    path('coupons/', views.admin_coupons_view, name='coupons'),
    path('add-coupon/', views.add_coupon_view, name='add-coupon'),
    path('edit-coupon/<id>/', views.edit_coupon_view, name='edit-coupon'),
    path('delete-coupon/<id>/', views.delete_coupon_view, name='delete-coupon'),
    path('contact-us/', views.admin_contact_us_view, name='contact-us'),
    path('contact-detail/<id>/', views.contact_detail_view, name='contact-detail'),
    path('contact-status/<id>/', views.change_contact_status, name='contact-status'),
    path('delete-contact/<id>/', views.contact_delete_view, name='delete-contact'),
    path('users/', views.admin_users_view, name='users'),
    path('add-user/', views.add_user_view, name='add-user'),
    path('edit-user/<id>/', views.edit_user_view, name='edit-user'),
    path('delete-user/<id>/', views.delete_user_view, name='delete-user'),
    path('suppliers/', views.admin_suppliers_view, name='suppliers'),
    path('add-supplier/', views.add_supplier_view, name='add-supplier'),
    path('edit-supplier/<sid>/', views.edit_supplier_view, name='edit-supplier'),
    path('delete-supplier/<sid>/', views.delete_supplier_view, name='delete-supplier'),
    path('settings/', views.admin_settings_view, name='settings'),
    path('change-password/', views.admin_change_password, name='change-password'),

    path("export-sales-report/", views.export_sales_report, name="export-sales-report"),

]