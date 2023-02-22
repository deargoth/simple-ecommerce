from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from .models import Product, Variation
from pprint import pprint


class Index(ListView):
    model = Product
    template_name = 'product/index.html'
    paginate_by = 6
    context_object_name = 'products'


class Details(DetailView):
    model = Product
    template_name = 'product/detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'


class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META['HTTP_REFERER']

        vid = self.request.GET.get('vid')

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        variation = Variation.objects.get(id=vid)
        product = Product.objects.get(id=variation.product.pk)

        variation_stock = variation.stock

        product_id = product.pk
        product_name = product.name
        variation_name = variation.name
        variation_id = variation.pk
        unit_price = variation.price
        promotional_unit_price = variation.promotional_price
        quantity = 1
        slug = product.slug
        image = product.image.name

        if str(variation_id) in cart:
            cart_quantity = cart[vid]['quantity']
            unit_price = cart[vid]['unit_price']
            promotional_unit_price = cart[vid]['promotional_unit_price']

            if cart_quantity > variation_stock:
                messages.error(self.request,
                               f'O estoque do produto {product_name} foi excedido. Adicionamos {variation_stock}x\
                                   em seu carrinho.')

                cart_quantity = variation_stock

            cart_quantity += 1

            cart[vid]['quantity'] = cart_quantity
            cart[vid]['quant_price'] = unit_price * cart_quantity
            cart[vid]['promotional_quant_price'] = promotional_unit_price * cart_quantity

        else:
            cart[vid] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unit_price': unit_price,
                'promotional_unit_price': promotional_unit_price,
                'quant_price': unit_price,
                'promotional_quant_price': promotional_unit_price,
                'quantity': 1,
                'slug': slug,
                'image': image
            }

        pprint(cart)
        self.request.session.save()

        return redirect(http_referer)
