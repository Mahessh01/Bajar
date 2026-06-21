from .models import CartItem

def counter(request):
    cart_count = 0

    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(
            user=request.user,
            is_active=True
        ).count()

    return {'cart_count': cart_count}