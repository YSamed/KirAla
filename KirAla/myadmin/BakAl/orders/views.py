from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderItem
from products.models import Product
from .forms import OrderItemForm
from django.contrib import messages

@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-order_date')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})







@login_required
def create_order_from_cart(request):
    order, created = Order.objects.get_or_create(customer=request.user, shipping_status='pending')

    cart_items = request.user.cart.items.all()

    try:
        for cart_item in cart_items:
            order_item, created = OrderItem.objects.get_or_create(order=order, product=cart_item.product)
            order_item.quantity += cart_item.quantity
            order_item.save()
            cart_item.delete()

        order.place_order()

        new_cart = Cart.objects.create(user=request.user)

        return redirect('orders:order_detail', order_id=order.id)

    except Exception as e:
        messages.error(request, f"Sipariş oluşturulurken bir hata oluştu: {str(e)}")
        return redirect('products:view_cart')



