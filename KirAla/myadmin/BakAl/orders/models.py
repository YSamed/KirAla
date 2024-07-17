from time import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from products.models import Product

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('processing', 'İşleniyor'),
        ('shipped', 'Kargoya Verildi'),
        ('completed', 'Tamamlandı'),
        ('canceled', 'İptal Edildi'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    shipping_address = models.TextField(null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Sipariş #{self.id} - Müşteri: {self.customer.username}"

    def update_total_price(self):
        total = sum(item.get_total_price() for item in self.order_items.all())
        self.total_price = total
        self.save()

    def place_order(self):
        try:
            for item in self.order_items.all():
                if item.quantity > item.product.stock:
                    raise ValidationError(f"{item.product.name} stokta yeterli değil.")
                item.product.stock -= item.quantity
                item.product.save()
            self.shipping_status = 'processing'
            self.is_paid = True  # Ödeme doğrulandı
            self.payment_date = timezone.now()
            self.save()
        except ValidationError as e:
            self.shipping_status = 'canceled'
            self.save()
            raise e
    
    def cancel_order(self):
        for item in self.order_items.all():
            item.product.stock += item.quantity
            item.product.save()
        self.shipping_status = 'canceled'
        self.save()

    def prepare_order(self):
        for item in self.order_items.all():
            item.product.stock -= item.quantity
            item.product.save()
        self.shipping_status = 'processing'
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=True)

    class Meta:
        unique_together = ('order', 'product')

    def clean(self):
        if not self.product.is_active:
            raise ValidationError(_('Bu ürün şu anda aktif değil ve sepete eklenemez.'))
        if self.quantity is None or self.quantity <= 0:
            raise ValidationError(_('Geçerli bir miktar giriniz.'))
        if self.product.stock is None or not isinstance(self.product.stock, int) or self.quantity > self.product.stock:
            raise ValidationError(f"{self.product.name} stokta yeterli değil veya stok belirtilmedi.")

    def save(self, *args, **kwargs):
        self.clean()
        self.price = self.product.price
        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.order.customer.username} - {self.product.name} - {self.quantity} adet"

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total_price(sender, instance, **kwargs):
    instance.order.update_total_price()

@receiver(post_save, sender=OrderItem)
def update_stock_on_save(sender, instance, **kwargs):
    instance.product.stock -= instance.quantity
    instance.product.save()

@receiver(post_delete, sender=OrderItem)
def update_stock_on_delete(sender, instance, **kwargs):
    instance.product.stock += instance.quantity
    instance.product.save()



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} adet"
