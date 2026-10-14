from .models import Category


def categories_processor(request):
    """
    Exposes active categories across all templates for navigation.
    """
    active_categories = Category.objects.filter(is_active=True).order_by('name')
    return {
        'nav_categories': active_categories,
    }
