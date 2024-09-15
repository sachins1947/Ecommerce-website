from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404

# Create your views here.
def store(request, category_slug=None):
    number_per_product_pag = 6
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')

    paginator = Paginator(products, number_per_product_pag)
    page = request.GET.get('page')

    try:
        paged_products = paginator.get_page(page)
    except PageNotAnInteger:
        paged_products = paginator.get_page(1)
    except EmptyPage:
        paged_products = paginator.get_page(paginator.num_pages)

    products_count = products.count()

    context = {
        'products': paged_products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Product.DoesNotExist:
        raise Http404("Product not found")

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    products = Product.objects.none()  # Initialize with an empty queryset
    
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )

    products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)
