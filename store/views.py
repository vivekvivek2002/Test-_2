from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product, Banner


def home(request):
    return HttpResponse("AURA Storefront")


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    return HttpResponse(f"Category: {category.name}")


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return HttpResponse(f"Product: {product.name}")
