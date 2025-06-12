from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import F
from django.contrib.auth.decorators import login_required
from userauths.models import User, Contact
from core.forms import AddressForm
from .services import apply_filters, apply_sorting, paginate_products
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from core.models import Coupon, Product, ProductImages, Category, Address, Supplier, CartOrder, CartOrderItem, Brand
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
    categories = Category.objects.all()
    internal_images = product.internal_images.all()

    context = {
        'p': product,
        'internal_images': internal_images,
        'products': products,
        'categories': categories,
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
                    'pid': pid,
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
    categories = Category.objects.all()

    cart_total_amount = 0
    cart_data = request.session.get('cart_data_obj', {})

    if cart_data:
        for pid, item in cart_data.items():
            cart_total_amount += int(item['qty']) * float(item['price'])


        return render(request, 'core/cart.html', {
            'cart_data': cart_data,
            'cart_total_amount': cart_total_amount,
            'cart_total_items': len(cart_data),
            'categories': categories,
        })
    else:
        messages.warning(request, "Your cart is empty.")
        return redirect('core:index')

def delete_cart_item(request):
    product_id = request.GET.get('pid')

    cart = request.session.get('cart_data_obj', {})

    if product_id in cart:
        del cart[product_id]
        request.session['cart_data_obj'] = cart

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string('core/async/cart_list.html', {
        'cart_data': request.session['cart_data_obj'],
        'cart_total_amount': cart_total_amount,
        'cart_total_items': len(request.session['cart_data_obj']),
    })

    return JsonResponse({'data': context, 'cart_total_items': len(request.session['cart_data_obj'])})
   
def update_cart_item(request):
    product_id = request.GET.get('pid')
    quantity = int(request.GET.get('quantity', 1))
    cart = request.session.get('cart_data_obj', {})

    if product_id in cart:
        cart[product_id]['qty'] = quantity
        request.session['cart_data_obj'] = cart

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string('core/async/cart_list.html', {
        'cart_data': request.session['cart_data_obj'],
        'cart_total_amount': cart_total_amount,
        'cart_total_items': len(request.session['cart_data_obj']),
    })

    return JsonResponse({'data': context, 'cart_total_items': len(request.session['cart_data_obj'])})

def apply_coupon(request):
    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')

        coupon = Coupon.objects.filter(code=coupon_code, active=True).first()
        if not coupon:
            return JsonResponse({'success': False, 'message': 'Invalid coupon code'})

        cart_total_amount = 0
        if 'cart_data_obj' in request.session:
            for pid, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * Decimal(item['price'])
        else:
            return JsonResponse({'success': False, 'message': 'Cart is empty'})

        discount = cart_total_amount * (coupon.discount_percentage / Decimal('100'))
        total_after_discount = cart_total_amount - discount

        request.session['applied_coupon'] = coupon.code

        return JsonResponse({
            'success': True,
            'discount': round(discount, 2),
            'total_after_discount': round(total_after_discount, 2),
            'cart_total_amount': round(cart_total_amount, 2),
            'message': 'Coupon applied successfully',
        })

@login_required
def checkout_view(request):
    categories = Category.objects.all()
    payment_method = request.POST.get('payment_method')

    cart_total_amount = 0
    cart_data = request.session.get('cart_data_obj', {})
    for pid, item in cart_data.items():
        cart_total_amount += int(item['qty']) * Decimal(item['price'])

    # نحسب الخصم
    applied_coupon_code = request.session.get('applied_coupon')
    discount = Decimal('0.00')
    coupon = None 
    if applied_coupon_code:
        coupon = Coupon.objects.filter(code=applied_coupon_code, active=True).first()
        if coupon:
            discount = cart_total_amount * (coupon.discount_percentage / Decimal('100'))
        else:
            del request.session['applied_coupon']


    address_form = AddressForm()
    if request.method == 'POST':
        address_form = AddressForm(request.POST)

        if address_form.is_valid():
            messages.success(request, "Address form is valid ✅")

            address = address_form.save(commit=False)
            address.user = request.user
            address.save()

            # إنشاء الأوردر بعد نجاح الفورم
            order = CartOrder.objects.create(
                user=request.user,
                price=cart_total_amount,
                saved=discount,
                total_price=cart_total_amount - discount,
                order_status='Pending',
                address=address,
                paid_status=False
            )
            messages.success(request, f"Order created successfully with ID: {order.oid}")

            for pid, item in cart_data.items():
                CartOrderItem.objects.create(
                    order=order,
                    product_id=item['pid'],
                    image=item['image'],
                    quantity=item['qty'],
                    price=item['price'],
                    total_price=Decimal(item['qty']) * Decimal(item['price']),
                    invoice_number=f"INV_NO-{order.oid}-{pid}"
                )

            if applied_coupon_code and coupon:
                order.coupons.add(coupon)
                messages.success(request, "Coupon applied to order.")

            # تفريغ السلة
            del request.session['cart_data_obj']
            if 'applied_coupon' in request.session:
                del request.session['applied_coupon']

            if payment_method == "COD":
                messages.success(request, "Order placed successfully. Cash on Delivery.")
                return redirect('core:invoice')
            else:
                messages.error(request, "please choose payment method.")
                return redirect('core:checkout')

        else:
            # لو الفورم مش valid نعرض الأخطاء
            messages.error(request, f"Address form is invalid: {address_form.errors}")

    return render(request, 'core/checkout.html', {
        'cart_data': cart_data,
        'cart_total_amount': round(cart_total_amount, 2),
        'cart_total_items': len(cart_data),
        'discount': round(discount, 2),
        'categories': categories,
        'address_form': address_form,
    })


def invoice_view(request):
    categories = Category.objects.all()
    
    # Get the most recent order for the user
    try:
        order = CartOrder.objects.filter(user=request.user).order_by('-order_date').first()
    except CartOrder.DoesNotExist:
        order = None
    order_items = CartOrderItem.objects.filter(order__user=request.user).order_by('-id')
    context = {
        'order': order,
        'order_items': order_items,
        'categories': categories,
    }
    

    return render(request, 'core/invoice.html', context)


def contact_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'core/contact.html', context)

def Ajax_contact_form(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        

        Contact.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message
        )

        data={
            'success': True,
            'message': 'Message Sent Successfully!',
        }
        return JsonResponse(data)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})