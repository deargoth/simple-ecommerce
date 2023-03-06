from django.shortcuts import render, redirect
from .models import Product, Variation
from django.views.generic import ListView, DetailView, View
from pprint import pprint
from utils import ec_messages
from django.contrib import messages


class Index(ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'
    paginate_by = 3


class Details(DetailView):
    model = Product
    template_name = 'product/details.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META['HTTP_REFERER']

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session.get('cart')

        if 'vid' in self.request.GET.keys():
            vid = self.request.GET.get('vid')
            variation = Variation.objects.get(id=vid)
            variation_stock = variation.stock
            product = variation.product

            product_name = product.name
            product_id = product.pk
            variation_name = variation.name
            variation_pk = variation.pk
            variation_price = variation.price
            variation_promotional_price = variation.promotional_price

            if variation.image:
                variation_image = variation.image.name
            else:
                variation_image = product.image.name

            slug = product.slug
            quantity = 1

            if vid not in cart.keys():
                cart[vid] = {
                    'product_name': product_name,
                    'product_id': product_id,
                    'variation_name': variation_name,
                    'variation_pk': variation_pk,
                    'unit_price': variation_price,
                    'promotional_unit_price': variation_promotional_price,
                    'quant_price': variation_price,
                    'promotional_quant_price': variation_promotional_price,
                    'slug': slug,
                    'quantity': 1,
                    'image': variation_image,
                }

            else:
                cart_quantity = cart[vid]['quantity']
                product_stock = variation_stock
                unit_price = cart[vid]['unit_price']
                promotional_unit_price = cart[vid]['promotional_unit_price']
                cart_quantity += 1

                if cart_quantity >= product_stock:
                    messages.error(self.request,
                                   ec_messages.error_quantity_exceeded)
                    cart_quantity = product_stock

                cart[vid]['quantity'] = cart_quantity
                cart[vid]['quant_price'] = unit_price * cart_quantity
                cart[vid]['promotional_quant_price'] = promotional_unit_price * cart_quantity

        elif 'pid' in self.request.GET.keys():
            pid = self.request.GET.get('pid')
            product = Product.objects.get(id=pid)
            db_stock = product.stock

            product_name = product.name
            product_id = product.pk
            product_price = product.price
            product_promotional_price = product.promotional_price
            image = product.image.name
            slug = product.slug

            if pid not in cart.keys():
                cart[pid] = {
                    'product_name': product_name,
                    'product_id': product_id,
                    'unit_price': product_price,
                    'promotional_unit_price': product_promotional_price,
                    'quant_price': product_price,
                    'promotional_quant_price': product_promotional_price,
                    'slug': slug,
                    'quantity': 1,
                    'image': image,
                }

            else:
                cart_quantity = cart[pid]['quantity']
                product_stock = db_stock
                unit_price = cart[pid]['unit_price']
                promotional_unit_price = cart[pid]['promotional_unit_price']
                cart_quantity += 1

                if cart_quantity >= product_stock:
                    messages.error(self.request,
                                   ec_messages.error_quantity_exceeded)
                    cart_quantity = product_stock

                cart[pid]['quantity'] = cart_quantity
                cart[pid]['quant_price'] = unit_price * cart_quantity
                cart[pid]['promotional_quant_price'] = promotional_unit_price * cart_quantity

        pprint(cart)
        self.request.session.save()

        return redirect(http_referer)
