# core/utils.py
from django.db.models import F
from django.core.paginator import Paginator

def apply_filters(request, products):
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price and max_price:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            products = products.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass

    if request.GET.get("in_stock") == "true":
        products = products.filter(in_stock=True)

    if request.GET.get("on_sale") == "true":
        products = products.filter(old_price__gt=0, price__lt=F('old_price'))

    brand_ids = request.GET.getlist("brands[]")
    if brand_ids:
        products = products.filter(brand__bid__in=brand_ids)

    return products


def apply_sorting(request, products):
    sort_by = request.GET.get("sort_by")
    if sort_by == "price_asc":
        return products.order_by("price")
    elif sort_by == "price_desc":
        return products.order_by("-price")
    elif sort_by == "latest":
        return products.order_by("-created_at")
    elif sort_by == "best_selling":
        return products.order_by("-quantity_sold")
    return products.order_by("-created_at")


def paginate_products(request, products, per_page=6):
    query_dict = request.GET.copy()
    query_dict.pop("page", None)
    query_string = query_dict.urlencode()

    paginator = Paginator(products, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj, query_string
