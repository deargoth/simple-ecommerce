from django.contrib import admin
from .models import Order, OrderItem


class OrderInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
