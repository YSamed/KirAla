from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404 ,redirect
from .models import Category, Product
from orders.models import Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def product_list(request, category_id=None):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        descendant_categories = category.get_descendants(include_self=True)
        products = products.filter(category__in=descendant_categories)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order = Order.objects.filter(customer=request.user, shipping_status='pending').first()

    if not order:
        order = Order.objects.create(customer=request.user, shipping_status='pending')

    try:
        order_item = OrderItem.objects.get(order=order, product=product)
        order_item.quantity += 1
        order_item.save()
    except OrderItem.DoesNotExist:
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1)

    messages.success(request, f"{product.name} başarıyla sepetinize eklendi.")
    return redirect('products:view_cart')


@login_required
def view_cart(request):
    order = Order.objects.filter(customer=request.user, shipping_status='pending').first()
    if order:
        order_items = order.order_items.all()
        total_price = sum(item.get_total_price() for item in order_items)

        if request.method == 'POST' and 'place_order' in request.POST:
            order.prepare_order()  
            messages.success(request, "Siparişiniz başarıyla oluşturuldu. Ürünler hazırlanıyor.")

    else:
        order_items = []
        total_price = 0

    return render(request, 'orders/cart.html', {'order_items': order_items, 'total_price': total_price})



@login_required
def remove_from_cart(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order_item.delete()
    messages.success(request, f"{order_item.product.name} sepetten başarıyla çıkarıldı.")
    return redirect('products:view_cart')

@login_required
def increase_quantity(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order_item.quantity += 1
    order_item.save()
    messages.success(request, f"{order_item.product.name} adeti bir artırıldı.")
    return redirect('products:view_cart')



def checkout(request):
    order = Order.objects.filter(customer=request.user, shipping_status='pending').first()
    if order:
        order.shipping_status = 'processing'
        order.save()
    
        messages.success(request, 'Siparişiniz başarıyla tamamlandı!')

    return redirect('products:product_list')  


