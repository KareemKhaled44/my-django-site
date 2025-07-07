from django.shortcuts import render
import datetime
from django.shortcuts import redirect
from core.models import Product, Category, CartOrder, CartOrderItem, Brand, Flavor
from django.db.models import Sum
from userauths.models import User, Contact
from core.services import paginate_products
from useradmin.forms import AddProductForm, AddCategoryForm, AddBrandForm, AddFlavorForm
from userauths.forms import PasswordChangeForm
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Count, F
import json
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
# Create your views here.

def dashboard(request):
    revenue = CartOrder.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders_count = CartOrder.objects.count()
    all_products = Product.objects.all()
    low_stock_products = Product.objects.filter(quantity__lte=5)
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by('id')[:5]
    latest_orders = CartOrder.objects.all().order_by('-order_date')[:5]


    this_month = datetime.datetime.now().month
    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(Sum('total_price'))['total_price__sum'] or 0


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
        products = Product.objects.all().order_by('-pid')

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
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        form.save_m2m() 
        return redirect('useradmin:products')
    else:
        from django.contrib import messages
        messages.error(request, "Form is not valid. Please check the errors below.")
        print(form.errors)
        form = AddProductForm()
    return render(request, 'useradmin/add_product.html', {'form': form})

def edit_product_view(request, pid):
    product = Product.objects.get(pid=pid)
    form = AddProductForm(request.POST or None, request.FILES or None, instance=product)
    
    if request.method == 'POST' and form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        form.save_m2m() 
        return redirect('useradmin:products')
    else:
        from django.contrib import messages
        messages.error(request, "Form is not valid. Please check the errors below.")
        print(form.errors)
        form = AddProductForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'useradmin/edit_product.html', context )

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
        
def admin_contact_us_view(request):
    contact = Contact.objects.all()
    order = CartOrder.objects.all().order_by('-order_date') 

    if 'q' in request.GET:
        query = request.GET.get('q')
        search_mode = bool(query)
        contact = Contact.objects.filter(name__icontains=query)
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
def admin_settings_view(request):
    return render(request, 'useradmin/settings.html')