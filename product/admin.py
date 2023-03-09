from django.contrib import admin
from .models import Product, Variation


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


class VariationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'promotional_price',
                    'slug', 'stock', 'type')
    inlines = [
        VariationInline,
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
