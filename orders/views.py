from datetime import date

from django.shortcuts import redirect, render

from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order

# Create your views here.
def place_order(request, total=0,quantity=0):
    current_user= request.user
    
    cart_items = CartItem.objects.filter(user= current_user)
    cart_count= cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total= 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax= (2*total)/100
    grand_total= total + tax
    
    if request.method == 'POST':
        form= OrderForm(request.POST)
        if form.is_valid():
            #storing billing info
            data= Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address = form.cleaned_data['address']
            data.order_note = form.cleaned_data['order_note']
            data.order_total= grand_total
            data.tax= tax
            data.ip= request.META.get('REMOTE_ADDR')
            data.user = current_user
            data.save()

            # Generate order number
            current_date = date.today().strftime('%Y%m%d')
            data.order_number = f"{current_date}{data.id}"

            # Save only the order number
            data.save(update_fields=['order_number'])
            return redirect('checkout')
        else:
            return redirect('checkout')

        
            

            



