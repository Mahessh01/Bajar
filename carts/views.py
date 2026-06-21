from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from store.models import Product, Variation
from .models import CartItem


# -------------------------
# ADD TO CART
# -------------------------
def add_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    # Get selected variations
    if request.method == 'POST':
        for key, value in request.POST.items():

            if key == 'csrfmiddlewaretoken':
                continue

            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)

            except Variation.DoesNotExist:
                pass

    # User must be logged in
    if request.user.is_authenticated:

        cart_items = CartItem.objects.filter(
            product=product,
            user=request.user,
            is_active=True
        ).prefetch_related('variations')

        for cart_item in cart_items:

            existing_variations = list(
                cart_item.variations.all().order_by('id')
            )

            new_variations = sorted(
                product_variation,
                key=lambda x: x.id
            )

            if existing_variations == new_variations:
                cart_item.quantity += 1
                cart_item.save()
                return redirect('cart')

        # Create new cart item if no match found
        cart_item = CartItem.objects.create(
            product=product,
            user=request.user,
            quantity=1,
            is_active=True
        )

        if product_variation:
            cart_item.variations.add(*product_variation)

    return redirect('cart')


# -------------------------
# REMOVE ONE ITEM
# -------------------------
def remove_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart_item = CartItem.objects.filter(
        product=product,
        user=request.user,
        is_active=True
    ).first()

    if cart_item:

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()

    return redirect('cart')


# -------------------------
# DELETE CART ITEM COMPLETELY
# -------------------------
def remove_cart_item(request, cart_item_id):

    cart_item = CartItem.objects.get(
        id=cart_item_id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart')


# -------------------------
# CART PAGE
# -------------------------
def cart(request):

    total = 0
    quantity = 0

    if request.user.is_authenticated:

        cart_items = CartItem.objects.filter(
            user=request.user,
            is_active=True
        ).prefetch_related('variations')

        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity

    else:
        cart_items = CartItem.objects.none()

    tax = (2 * total) / 100
    grand_total = total + tax

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)


# -------------------------
# CHECKOUT
# -------------------------
@login_required(login_url='login')
def checkout(request):

    total = 0
    quantity = 0

    cart_items = CartItem.objects.filter(
        user=request.user,
        is_active=True
    ).prefetch_related('variations')

    for item in cart_items:
        total += item.product.price * item.quantity
        quantity += item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/checkout.html', context)

def increase_cart(request, cart_item_id):

    cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


def decrease_cart(request, cart_item_id):

    cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')