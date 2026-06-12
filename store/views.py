from django.shortcuts import get_object_or_404, render
from carts.models import CartItem
from category.models import Category
from .models import Product
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def store(request, category_slug=None):
    categories = None
    products = None

    # If category is selected (filtered store page)
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        
    else:
        # Show all available products
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    # Count products safely
    product_count = products.count()

    # Context data sent to template
    context = {
        'products': paged_products,
        'product_count': product_count,
        'categories': categories,
        
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try: 
        single_product = Product.objects.get(category__slug = category_slug,slug= product_slug)
        in_cart= CartItem.objects.filter(cart__cart_id=_cart_id(request),product = single_product).exists()
    except Exception as e:
        raise e
    context= { 
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request,'store/product_detail.html',context)

