from decimal import Decimal
from django.shortcuts import render
import datetime
from django.shortcuts import redirect
from core.models import Product, ProductImages, Category, CartOrder, CartOrderItem, Brand, Flavor, Address, Coupon, Supplier
from django.db.models import Sum
from userauths.models import User, Contact
from core.services import paginate_products
from useradmin.forms import AddProductForm, AddCartOrderForm, AddOrderItemForm, AddCategoryForm, AddBrandForm, AddFlavorForm, AddAddressForm, AddCouponForm, AddSupplierForm
from userauths.forms import PasswordChangeForm, ProfileEditForm, UserRegistrationForm
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Count, F
import json
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
# Create your views here.

def dashboard(request):
    revenue = CartOrder.objects.filter(paid_status=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders_count = CartOrder.objects.count()
    paid_orders = CartOrder.objects.filter(paid_status=True).count()
    all_products = Product.objects.all()
    low_stock_products = Product.objects.filter(quantity__lte=5)
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by('id')[:5]
    latest_orders = CartOrder.objects.all().order_by('-order_date')[:5]

    total_profit = CartOrderItem.objects.filter(order__paid_status=True).aggregate(Sum('profit'))['profit__sum'] or 0

    this_month = datetime.datetime.now().month

    monthly_revenue = CartOrder.objects.filter(
        paid_status=True,
        order_date__month=this_month
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0

    orders= CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('oid')).values('month', 'count').order_by('month')
    month=[]
    total_orders = []
    for order in orders:
        month.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])


    in_stock = Product.objects.filter(in_stock=True).count()
    out_stock = Product.objects.filter(in_stock=False).count()  
        
    context = {
        'revenue': revenue,
        'total_orders_count': total_orders_count,
        'paid_orders': paid_orders,
        'all_products': all_products,
        'low_stock_products': low_stock_products,
        'all_categories': all_categories,
        'new_customers': new_customers,
        'latest_orders': latest_orders,
        'month': json.dumps(month),
        'orders_count': json.dumps(total_orders),
        'in_out_stock_data': json.dumps([in_stock, out_stock]),
        'in_out_stock_labels': json.dumps(["instock", "outstock"]),
        'total_orders_count': total_orders_count,
        'total_profit': total_profit,
        'monthly_revenue': monthly_revenue,
    }
    return render(request, 'useradmin/dashboard.html', context)

def admin_products_view(request):
    all_categories = Category.objects.all()

    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        products = Product.objects.filter( title__icontains=query)

    else:
        search_mode = False
        products = Product.objects.all().order_by('-created_at')

    # Apply pagination 
    page_obj, query_string = paginate_products(request, products, per_page=8)

    context = {
        'products': page_obj.object_list,
        'all_categories': all_categories,
        'search_mode': search_mode,
        'page_obj': page_obj,
        'query_string': query_string,
    }
    return render(request, 'useradmin/products.html', context)

def add_product_view(request):
    form = AddProductForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        form.save_m2m()

        # Handle multiple internal images
        for file in request.FILES.getlist('internal_images'):
            ProductImages.objects.create(product=product, image=file)
        return redirect('useradmin:products')
    else:
        messages.error(request, "Form is not valid. Please check the errors below.")
        messages.error(request, form.errors)
        form = AddProductForm()
    return render(request, 'useradmin/add_product.html', {'form': form})

def edit_product_view(request, pid):
    product = Product.objects.get(pid=pid)
    form = AddProductForm(request.POST or None, request.FILES or None, instance=product)
    
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        form.save_m2m() 

        # Handle multiple internal images
        for file in request.FILES.getlist('internal_images'):
            ProductImages.objects.create(product=product, image=file)

        return redirect('useradmin:products')
    else:
        messages.error(request, "Form is not valid. Please check the errors below.")
        form = AddProductForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'useradmin/edit_product.html', context )

def delete_internal_image(request, img_id):
    img = ProductImages.objects.get(id=img_id)
    pid = img.product.pid
    img.delete()
    messages.success(request, "Image deleted.")
    return redirect('useradmin:edit-product', pid=pid)

def delete_product_view(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect('useradmin:products')

def admin_orders_view(request):
    all_orders = CartOrder.objects.all().order_by('-order_date')
    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        orders = CartOrder.objects.filter(oid__icontains=query)
    else:
        search_mode = False
        orders = CartOrder.objects.all().order_by('-order_date')

    # Apply pagination if needed
    page_obj, query_string = paginate_products(request, orders, per_page=8)

    context = {
        'orders': page_obj.object_list,
        'search_mode': search_mode,
        'page_obj': page_obj,
        'query_string': query_string,
    }
    return render(request, 'useradmin/orders.html', context)

def order_detail_view(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItem.objects.filter(order=order)
    
    # Calculate total price for the order
    sub_total = sum(item.price * item.quantity for item in order_items)

    context = {
        'order': order,
        'order_items': order_items,
        'sub_total': sub_total,
    }
    return render(request, 'useradmin/order_detail.html', context)

def change_order_status(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if request.method == 'POST':
        new_status = request.POST.get('status')  
        order.order_status  = new_status
        order.save()
        messages.success(request, f"Order status updated to {new_status}.")
        return redirect('useradmin:order-detail', oid=oid)
    else:
        messages.error(request, "Invalid request method.")
    return redirect('useradmin:order-detail', oid=oid)

def change_order_paid_status(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if request.method == 'POST':
        new_status = request.POST.get('paid_status')  # "true" or "false"
        order.paid_status = new_status == "true"  # Convert to boolean
        order.save()
        messages.success(request, f"Order paid status updated.")
        return redirect('useradmin:order-detail', oid=oid)
    else:
        messages.error(request, "Invalid request method.")
    return redirect('useradmin:order-detail', oid=oid)

def add_order_view(request):
    form = AddCartOrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.save()
        return redirect('useradmin:add-order-items', oid=order.oid)  # Redirect to Step 2
    return render(request, 'useradmin/add_order.html', {'form': form})

def add_order_items_view(request, oid):
    order = CartOrder.objects.get(oid=oid)
    form = AddOrderItemForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.order = order
        item.price = item.product.price
        item.total_price = item.price * item.quantity
        item.profit = (item.price - item.product.buying_price) * item.quantity
        item.image = item.product.image  # optional
        item.save()

        product = item.product
        product.quantity -= item.quantity
        product.quantity_sold += item.quantity
        product.save()

        update_order_totals(order) # Update order totals after adding item
        return redirect('useradmin:add-order-items', oid=oid)

    items = CartOrderItem.objects.filter(order=order)

    context = {
        'form': form,
        'order': order,
        'items': items,
    }
    return render(request, 'useradmin/add_order_items.html', context)

def update_order_totals(order):
    items = CartOrderItem.objects.filter(order=order)
    subtotal = sum(item.total_price for item in items)

    total_discount = 0
    if order.coupons and order.coupons.active:
        discount = (subtotal * order.coupons.discount_percentage) / 100
        total_discount += discount

    # Shipping rules
    if subtotal < 500:
        shipping_cost = 20
    elif subtotal < 1000:
        shipping_cost = 10
    else:
        shipping_cost = 0

    order.price = subtotal
    order.saved = discount
    order.shipping_cost = shipping_cost
    order.total_price = subtotal - discount + shipping_cost
    order.save()

def delete_order_item_view(request, oid, item_id):
    item = get_object_or_404(CartOrderItem, id=item_id, order__oid=oid)
    order = item.order
    item.delete()

    update_order_totals(order)

    messages.success(request, "Order item deleted successfully.")
    return redirect('useradmin:add-order-items', oid=order.oid)

def delete_order_view(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order.delete()
    messages.success(request, "Order deleted successfully.")
    return redirect('useradmin:orders')

def analytics_view(request):
    total_revenue = CartOrder.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    in_stock_products = Product.objects.filter(in_stock=True).count()
    total_orders_count = CartOrder.objects.count()

    avg_order_value = float(total_revenue / total_orders_count) if total_orders_count > 0 else 0

    orders = CartOrder.objects.annotate(
        month=ExtractMonth('order_date')
    ).values('month').annotate(
        count=Count('oid'),
        total=Sum('total_price')
    ).order_by('month')    
    month=[]
    total_orders = []
    revenue = []
    for order in orders:
        month.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])
        revenue.append(float(order['total']) if order['total'] else 0.0)

  
    # Top Selling Products (by revenue)
    top_products = CartOrderItem.objects.values(
        'product__title'  
    ).annotate(
        total_revenue=Sum(F('price') * F('quantity')),  # Calculate revenue per product
    ).order_by('-total_revenue')[:5]  # Top 5 products

    top_product_names = []
    top_product_revenue = []
   

    for product in top_products:
        top_product_names.append(product['product__title'])
        top_product_revenue.append(float(product['total_revenue']) if product['total_revenue'] else 0.0)
        

        
    in_stock = Product.objects.filter(in_stock=True).count()
    out_stock = Product.objects.filter(in_stock=False).count()  
    context = {
        'total_revenue': total_revenue,
        'in_stock_products': in_stock_products,
        'total_orders_count': total_orders_count,
        'avg_order_value': avg_order_value,
        'month': json.dumps(month),
        'orders_count': json.dumps(total_orders),
        'in_out_stock_data': json.dumps([in_stock, out_stock]),
        'in_out_stock_labels': json.dumps(["instock", "outstock"]),
        'revenue_data': json.dumps(revenue),
        'top_product_names': json.dumps(top_product_names),
        'top_product_revenue': json.dumps(top_product_revenue),
        
    }
    return render(request, 'useradmin/analytics.html', context)

def admin_categories_view(request):
    all_categories = Category.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        categories = Category.objects.filter(title__icontains=query)
    else:
        search_mode = False
        categories = Category.objects.all().order_by('-cid')

    # Apply pagination if needed
    # page_obj, query_string = paginate_products(request, categories, per_page=8)
    # For simplicity, we are not paginating categories here, but you can implement it if needed.

    context = {
        'categories': categories,
        'search_mode': search_mode,
        'all_categories': all_categories,
    }
    return render(request, 'useradmin/categories.html', context)

def add_category_view(request):
    form = AddCategoryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        return redirect('useradmin:category')
    else: 
        print(form.errors)
        form = AddCategoryForm()
    
    return render(request, 'useradmin/add_category.html', {'form': form})

def edit_category_view(request, cid):
    category = Category.objects.get(cid=cid)
    form = AddCategoryForm(request.POST or None, request.FILES or None, instance=category)
    
    if request.method == 'POST' and form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        return redirect('useradmin:category')
    else:
        print(form.errors)
        form = AddCategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'useradmin/edit_category.html', context)

def delete_category_view(request, cid):
    category = Category.objects.get(cid=cid)
    category.delete()
    return redirect('useradmin:category')

def admin_brands_view(request):
    all_brands = Brand.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        brands = Brand.objects.filter(name__icontains=query)
    else:
        search_mode = False
        brands = Brand.objects.all()

    context = {
        'brands': brands,
        'search_mode': search_mode,
        'all_brands': all_brands,
    }
    return render(request, 'useradmin/brands.html', context)

def add_brand_view(request):
    form = AddBrandForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        return redirect('useradmin:brand')
    else:
        form = AddBrandForm()
        
    return render(request, 'useradmin/add_brand.html', {'form': form})

def edit_brand_view(request, bid):
    brand = Brand.objects.get(bid=bid)
    form = AddBrandForm(request.POST or None, request.FILES or None, instance=brand)
    
    if request.method == 'POST' and form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        return redirect('useradmin:brand')
    else:
        print(form.errors)
        form = AddBrandForm(instance=brand)
    
    context = {
        'form': form,
        'brand': brand,
    }
    return render(request, 'useradmin/edit_brand.html', context)

def delete_brand_view(request, bid):
    brand = Brand.objects.get(bid=bid)
    brand.delete()
    return redirect('useradmin:brand')

def admin_flavors_view(request):
    all_flavors = Flavor.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        flavors = Flavor.objects.filter(name__icontains=query)
    else:
        search_mode = False
        flavors = Flavor.objects.all()

    context = {
        'flavors': flavors,
        'search_mode': search_mode,
        'all_flavors': all_flavors,
    }
    return render(request, 'useradmin/flavors.html', context)

def add_flavor_view(request):
    form = AddFlavorForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        return redirect('useradmin:flavor')
    else:
        form = AddFlavorForm()
    
    return render(request, 'useradmin/add_flavor.html', {'form': form})

def edit_flavor_view(request, id):
    flavor = Flavor.objects.get(id=id)
    form = AddFlavorForm(request.POST or None, instance=flavor)
    if request.method == 'POST' and form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        return redirect('useradmin:flavor')
    else:
        print(form.errors)
        form = AddFlavorForm(instance=flavor)
    context = {
        'form': form,
        'flavor': flavor,
    }
    return render(request, 'useradmin/edit_flavor.html', context)

def delete_flavor_view(request, id):
    flavor = Flavor.objects.get(id=id)
    flavor.delete()
    return redirect('useradmin:flavor')

def admin_addresses_view(request):
    all_addresses = Address.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        addresses = all_addresses.filter(first_name__icontains=query)
    else:
        search_mode = False
        addresses = all_addresses.order_by('-created_at')

    # Apply pagination if needed
    page_obj, query_string = paginate_products(request, addresses, per_page=8)

    context = {
        'addresses': page_obj.object_list,
        'search_mode': search_mode,
        'page_obj': page_obj,
        'query_string': query_string,
    }
    return render(request, 'useradmin/addresses.html', context)

def add_address_view(request):
    if request.method == 'POST':
        form = AddAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address added successfully!")
            return redirect('useradmin:addresses')
        else:
            messages.error(request, "Error adding address. Please check the form.")
    else:
        form = AddAddressForm()

    return render(request, 'useradmin/add_address.html', {'form': form})

def edit_address_view(request, id):
    address = Address.objects.get(id=id)
    if request.method == 'POST':
        form = AddAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully!")
            return redirect('useradmin:addresses')
        else:
            messages.error(request, "Error updating address. Please check the form.")
    else:
        form = AddAddressForm(instance=address)

    return render(request, 'useradmin/edit_address.html', {'form': form, 'address': address})

def delete_address_view(request, id):
    address = Address.objects.get(id=id)
    address.delete()
    messages.success(request, "Address deleted successfully!")
    return redirect('useradmin:addresses') 
        
def admin_coupons_view(request):
    coupons = Coupon.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        coupons = coupons.filter(code__icontains=query)
    else:
        search_mode = False
        coupons = coupons.order_by('-created_at')

    # Apply pagination if needed
    page_obj, query_string = paginate_products(request, coupons, per_page=8)

    context = {
        'coupons': page_obj.object_list,
        'search_mode': search_mode,
        'page_obj': page_obj,
        'query_string': query_string,
    }
    return render(request, 'useradmin/coupons.html', context)

def add_coupon_view(request):
    if request.method == 'POST':
        form = AddCouponForm(request.POST)
        if form.is_valid():
            coupon = form.save(commit=False)
            coupon.user = request.user
            coupon.save()
            messages.success(request, "Coupon added successfully!")
            return redirect('useradmin:coupons')
        else:
            messages.error(request, "Error adding coupon. Please check the form.")
    else:
        form = AddCouponForm()

    return render(request, 'useradmin/add_coupon.html', {'form': form})

def edit_coupon_view(request, id):
    coupon = Coupon.objects.get(id=id)
    if request.method == 'POST':
        form = AddCouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon updated successfully!")
            return redirect('useradmin:coupons')
        else:
            messages.error(request, "Error updating coupon. Please check the form.")
    else:
        form = AddCouponForm(instance=coupon)

    return render(request, 'useradmin/edit_coupon.html', {'form': form, 'coupon': coupon})

def delete_coupon_view(request, id):
    coupon = Coupon.objects.get(id=id)
    coupon.delete()
    messages.success(request, "Coupon deleted successfully!")
    return redirect('useradmin:coupons')

def admin_contact_us_view(request):
    contact = Contact.objects.all()
    order = CartOrder.objects.all().order_by('-order_date') 

    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        contact = Contact.objects.filter(full_name__icontains=query)
    else:
        search_mode = False
        contact = Contact.objects.all().order_by('-created_at')

    # Apply pagination if needed
    page_obj, query_string = paginate_products(request, contact, per_page=8)
    context = {
        'contact': page_obj.object_list,
        'search_mode': search_mode,
        'page_obj': page_obj,
        'query_string': query_string,
        'order': order,
    }
    return render(request, 'useradmin/contact_us.html', context)

def contact_delete_view(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    return redirect('useradmin:contact-us')

def contact_detail_view(request, id):
    contact = Contact.objects.get(id=id)
    context = {
        'contact': contact,
    }
    return render(request, 'useradmin/contact_detail.html', context)

def change_contact_status(request, id):
    contact = Contact.objects.get(id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')  
        contact.status = new_status
        contact.save()
        messages.success(request, f"Contact status updated to {new_status}.")
        return redirect('useradmin:contact-detail', id=id)
    else:
        messages.error(request, "Invalid request method.")
    return redirect('useradmin:contact-detail', id=id)

def admin_users_view(request):
    users = User.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        users = users.filter(username__icontains=query)
    else:
        search_mode = False
        users = users.order_by('-id')

    # Apply pagination if needed
    page_obj, query_string = paginate_products(request, users, per_page=8)

    context = {
        'users': page_obj.object_list,
        'search_mode': search_mode,
        'page_obj': page_obj,
        'query_string': query_string,
    }
    return render(request, 'useradmin/users.html', context)

def add_user_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "User added successfully!")
            return redirect('useradmin:users')
        else:
            messages.error(request, "Error adding user. Please check the form.")
    else:
        form = UserRegistrationForm()

    return render(request, 'useradmin/add_user.html', {'form': form})

def edit_user_view(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('useradmin:users')
        else:
            messages.error(request, "Error updating user. Please check the form.")
    else:
        form = UserRegistrationForm(instance=user)

    return render(request, 'useradmin/edit_user.html', {'form': form, 'user': user})

def delete_user_view(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('useradmin:users')

def admin_suppliers_view(request):
    suppliers = Supplier.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        suppliers = suppliers.filter(name__icontains=query)
    else:
        search_mode = False
        suppliers = suppliers.order_by('-sid')

    # Apply pagination if needed
    page_obj, query_string = paginate_products(request, suppliers, per_page=8)

    context = {
        'suppliers': page_obj.object_list,
        'search_mode': search_mode,
        'page_obj': page_obj,
        'query_string': query_string,
    }
    return render(request, 'useradmin/suppliers.html', context)

def add_supplier_view(request):
    if request.method == 'POST':
        form = AddSupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user  # Set the user who created the supplier
            supplier.save()
            messages.success(request, "Supplier added successfully!")
            return redirect('useradmin:suppliers')
        else:
            messages.error(request, "Error adding supplier. Please check the form.")
    else:
        form = AddSupplierForm()

    return render(request, 'useradmin/add_supplier.html', {'form': form})

def edit_supplier_view(request, sid):
    supplier = Supplier.objects.get(sid=sid)
    if request.method == 'POST':
        form = AddSupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier updated successfully!")
            return redirect('useradmin:suppliers')
        else:
            messages.error(request, "Error updating supplier. Please check the form.")
    else:
        form = AddSupplierForm(instance=supplier)

    return render(request, 'useradmin/edit_supplier.html', {'form': form, 'supplier': supplier})

def delete_supplier_view(request, sid):
    supplier = Supplier.objects.get(sid=sid)
    supplier.delete()
    messages.success(request, "Supplier deleted successfully!")
    return redirect('useradmin:suppliers')

def admin_settings_view(request):
    profile_form = ProfileEditForm(instance=request.user)

    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('useradmin:settings')
        else:
            messages.error(request, "Error updating profile. Please check the form.")

    else:
        profile_form = ProfileEditForm(instance=request.user)
    
    context = {
        'profile_form': profile_form,
    }
    return render(request, 'useradmin/settings.html', context)

def admin_change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('useradmin:dashboard')
        else:
            messages.error(request, "Error changing password. Please check the form.")
    else:
        password_form = PasswordChangeForm(request.user)
    return render(request, 'useradmin/change_password.html', {'password_form': password_form})


    # Assets
    cash = CartOrder.objects.filter(paid_status=True).aggregate(total=Sum('total_price'))['total'] or 0
    inventory = sum(
        p.buying_price * p.quantity for p in Product.objects.all()
        if p.buying_price and p.quantity
    )
    receivable = CartOrder.objects.filter(paid_status=False).aggregate(total=Sum('total_price'))['total'] or 0

    # Equity
    profit = CartOrderItem.objects.filter(order__paid_status=True).aggregate(total=Sum('profit'))['total'] or 0
    
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Balance Sheet"

    ws['A1'] = 'Balance Sheet'
    ws['A3'] = 'Assets'
    ws.append(['Cash', cash])
    ws.append(['Accounts Receivable', receivable])
    ws.append(['Inventory', inventory])

    ws.append([])
    ws.append(['Equity'])
    ws.append(['Retained Profit', profit])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=BalanceSheet.xlsx'
    wb.save(response)
    return response