from django.contrib import admin
from .models import Category, Product, CartItem, Order, OrderItem


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)


@admin.register(OrderItem)
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone', 'created_at')
    ordering = ('-created_at',)
    inlines = [OrderItemAdmin]
    readonly_fields = ('created_at',)


