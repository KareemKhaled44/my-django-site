from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import F
from .services import apply_filters, apply_sorting, paginate_products
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from core.models import Product, ProductImages, Category, Address, Supplier, CartOrder, CartOrderItem, Brand
# Create your views here.
def index(request):
    products= Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    best_sellers = Product.objects.filter(is_active=True).order_by('-quantity_sold')[:4]
    categories= Category.objects.all()
    context = {
        'products': products,
        'best_sellers': best_sellers,
        'categories': categories,
    }
    return render(request, 'core/index.html', context)

      
def product_list_view(request, cid=None):
    categories = Category.objects.all()
    brands = Brand.objects.all()

    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Product.objects.filter( title__icontains=query)
        template = 'core/search.html'
        context_extra = {'query': query}
    elif cid:
        selected_category = get_object_or_404(Category, cid=cid)
        products = Product.objects.filter(category__cid=cid)
        template = 'core/category-product-list.html'
        context_extra = {'category': selected_category}
    else:
        products = Product.objects.all()
        template = 'core/product-list.html'
        context_extra = {}

    # Apply filters and sorting
    products = apply_filters(request, products)
    products = apply_sorting(request, products)

    # Paginate
    page_obj, query_string = paginate_products(request, products, per_page=6)

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'query_string': query_string,
        **context_extra,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        product_html = render_to_string("core/async/product_card.html", context)
        pagination_html = render_to_string("core/async/pagination.html", context)
        return JsonResponse({"html": product_html, "pagination": pagination_html})

    return render(request, template, context)

def product_detail(request, pid):
    product= Product.objects.get(pid=pid)
    products=Product.objects.filter(category=product.category).exclude(pid=pid)[:5] #to show the same category products in the product detail page
    internal_images = product.internal_images.all()

    context = {
        'p': product,
        'internal_images': internal_images,
        'products': products,
    }
    return render(request, 'core/product-detail.html', context)

@require_GET
def search_products(request):
    q = request.GET.get('q', '')
    results = Product.objects.filter(title__icontains=q)[:10]
    data = [
        { 'id':p.pid, 'name': p.title, 'image': p.image.url, 'price': p.price}
        for p in results
    ]
    return JsonResponse(data, safe=False)


def add_to_cart(request):
    
    if request.method == 'GET':
        try:
            pid = str(request.GET.get('pid'))
            title = request.GET.get('product_title')
            quantity = int(request.GET.get('quantity'))
            price = float(request.GET.get('product_price'))
            image= request.GET.get('product_image')


            if 'cart_data_obj' not in request.session:
                request.session['cart_data_obj'] = {}

            cart_data = request.session['cart_data_obj']

            if pid in cart_data:
                cart_data[pid]['qty'] = int(cart_data[pid]['qty']) + quantity
            else:
                cart_data[pid] = {
                    'title': title,
                    'qty': quantity,
                    'price': price,
                    'image': image,
                }

            request.session['cart_data_obj'] = cart_data

            return JsonResponse({
                'data': cart_data,
                'cart_total_items': len(cart_data),
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_view(request):
    return render(request, 'core/cart.html')