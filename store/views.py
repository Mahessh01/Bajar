from django.shortcuts import get_object_or_404, render
from category.models import Category
from .models import Product


def store(request, category_slug=None):
    categories = None
    products = None

    # If category is selected (filtered store page)
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        # Show all available products
        products = Product.objects.filter(is_available=True)

    # Count products safely
    product_count = products.count()

    # Context data sent to template
    context = {
        'products': products,
        'product_count': product_count,
        'categories': categories,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try: 
        single_product = Product.objects.get(category__slug = category_slug,slug= product_slug)
    except Exception as e:
        raise e
    context= { 
        'single_product': single_product,
    }
    return render(request,'store/product_detail.html',context)