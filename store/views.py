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
    Displays active products for an active category.
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.filter(is_active=True)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """
    Displays product detail view with image, price, specs, and related products.
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
