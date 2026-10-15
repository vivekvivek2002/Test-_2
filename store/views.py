from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Banner


def home(request):
    """
    Database-driven homepage showcasing active hero banners,
    featured products, categories, and brand promotion.
    """
    banners = Banner.objects.filter(is_active=True).order_by('order', '-id')
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True,
        category__is_active=True
    ).select_related('category')[:8]
    categories = Category.objects.filter(is_active=True)

    context = {
        'banners': banners,
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def category_detail(request, slug):
    """
    Displays active products for an active category with optional sorting
    and availability filtering.
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products_qs = category.products.filter(is_active=True)

    # Filter by stock availability if requested
    stock_filter = request.GET.get('stock')
    if stock_filter == 'in_stock':
        products_qs = products_qs.filter(in_stock=True)

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_asc':
        products_qs = products_qs.order_by('price')
    elif sort_by == 'price_desc':
        products_qs = products_qs.order_by('-price')
    elif sort_by == 'name':
        products_qs = products_qs.order_by('name')
    else:
        # default: newest
        products_qs = products_qs.order_by('-created_at')

    context = {
        'category': category,
        'products': products_qs,
        'current_sort': sort_by,
        'current_stock': stock_filter,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """
    Displays product detail view with image, price, specs, availability, and related products.
    """
    product = get_object_or_404(
        Product.objects.select_related('category'),
        slug=slug,
        is_active=True,
        category__is_active=True
    )
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def custom_404(request, exception=None):
    """
    Custom 404 error page matching Aura Store's Apple-inspired minimalist aesthetic.
    """
    return render(request, '404.html', status=404)


def custom_500(request):
    """
    Custom 500 error page matching Aura Store's Apple-inspired minimalist aesthetic.
    """
    return render(request, '500.html', status=500)
