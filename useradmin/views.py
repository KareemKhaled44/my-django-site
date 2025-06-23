from django.shortcuts import render
import datetime
from django.shortcuts import redirect
from core.models import Product, Category, CartOrder
from django.db.models import Sum
from userauths.models import User
from core.services import paginate_products
from useradmin.forms import AddProductForm
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Count
import json
from django.utils.safestring import mark_safe
# Create your views here.

def dashboard(request):
    revenue = CartOrder.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders_count = CartOrder.objects.count()
    all_products = Product.objects.all()
    low_stock_products = Product.objects.filter(quantity__lte=5)
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by('id')[:5]
    latest_orders = CartOrder.objects.all().order_by('-oid')[:5]


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
