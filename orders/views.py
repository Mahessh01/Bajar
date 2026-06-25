from datetime import datetime

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
            data.first_name = form.cleaned_data('first_name')
            data.first_name = form.cleaned_data('last_name')
            data.first_name = form.cleaned_data('email')
            data.first_name = form.cleaned_data('phone')
            data.first_name = form.cleaned_data('address')
            data.first_name = form.cleaned_data('order_note')
            data.order_total= grand_total
            data.tax= tax
            data.ip= request.Meta.get('REMOTE_ADDR')
            data.save()
            
            #generate order number
            yr= int(datetime.date.today().strftime('%Y'))
            dt= int(datetime.date.today().strftime('%d'))
            mt= int(datetime.date.today().strftime('%m'))
            d= datetime.date(yr, mt, dt)
            current_date= d.strftime('%Y%m%d') #20210625
            order_number= current_date + str(data.id)
            data.order_number= order_number
            data.save()
            return redirect('checkout')
        else:
            return redirect('checkout')

        
            

            



