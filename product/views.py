from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from .models import Product, Variation
from django.http import HttpResponse
from pprint import pprint


class Index(ListView):
    model = Product
    template_name = 'product/index.html'
    paginate_by = 6
    context_object_name = 'products'
    ordering = '-id'


class Details(DetailView):
    model = Product
    template_name = 'product/detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(self.request)
    #     # context['variation'] = Variation.objects.get(
    #     #     product__slug__iexact=slug)

    #     return context


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

        if not variation_name:
            cart_add_message = f'O produto {product_name} foi adicionado ao seu carrinho com sucesso'

        else:
            cart_add_message = f'O produto {product_name} - {variation_name} foi adicionado ao seu carrinho com sucesso'

        if variation.stock == 0:
            messages.error(self.request,
                           'Infelizmente o estoque deste produto se esgotou')
            return redirect(reverse('product:details', kwargs={'slug': slug}))

        if str(variation_id) in cart:
            cart_quantity = cart[vid]['quantity']
            unit_price = cart[vid]['unit_price']
            promotional_unit_price = cart[vid]['promotional_unit_price']
            cart_quantity += 1

            if cart_quantity > variation_stock:
                messages.error(self.request,
                               f'O estoque do produto {product_name} foi excedido. Adicionamos {variation_stock}x\
                                   em seu carrinho.')

                cart[vid]['quantity'] = variation_stock
                self.request.session.save()
                return redirect(http_referer)

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

        self.request.session.save()

        messages.success(self.request,
                         cart_add_message)
        return redirect(http_referer)


class Cart(View):
    template_name = 'product/cart.html'

    def get(self, *args, **kwargs):
        self.context = {
            'cart': self.request.session.get('cart')
        }

        cart = self.context['cart']
        cart_keys = cart.keys()

        for key in cart_keys:
            if cart[key]['quantity'] == 0:
                removed_item = f'O produto {cart[key]["product_name"]} foi removido do seu carrinho'

                cart.pop(key)
                self.request.session.save()

                messages.error(self.request,
                               removed_item)

                return redirect('product:cart')

        return render(self.request, self.template_name, self.context)


class DelFromCart(View):
    def get(self, *args, **kwargs):
        cart = self.request.session.get('cart')
        vid_id = str(self.kwargs['pk'])

        quantity = cart[vid_id]['quantity']
        unit_price = cart[vid_id]['unit_price']
        promotional_unit_price = cart[vid_id]['promotional_unit_price']

        quantity -= 1

        if quantity <= 0:
            cart.pop(vid_id)
            self.request.session.save()
            return redirect('product:cart')

        cart[vid_id]['quantity'] = quantity
        cart[vid_id]['quant_price'] = unit_price * quantity
        cart[vid_id]['promotional_quant_price'] = promotional_unit_price * quantity

        self.request.session.save()
        return redirect('product:cart')


class Finalize(View):
    template_name = 'product/resume.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           'Você precisa estar logado para finalizar sua compra')
            return redirect('profile:create')

        if not self.request.session.get('cart'):
            messages.error(self.request,
                           'Seu carrinho está vaziado!')
            return redirect('product:index')

        self.context = {
            'user': self.request.user,
            'cart': self.request.session.get('cart'),
        }

        return render(self.request, self.template_name, self.context)
