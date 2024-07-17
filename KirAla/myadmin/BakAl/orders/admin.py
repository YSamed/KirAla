from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price',)
    fields = ('product', 'quantity', 'price')
    can_delete = True
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'shipping_status', 'total_price', 'is_paid')
    list_filter = ('shipping_status', 'is_paid', 'order_date')
    search_fields = ('customer__username',)
    inlines = [OrderItemInline]
    readonly_fields = ('order_date', 'total_price')

    def has_add_permission(self, request):
        return True

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
