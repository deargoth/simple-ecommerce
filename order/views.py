from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from .models import Order, OrderItem
from utils import utils
from django.contrib import messages
from product.models import Variation


class DispatchLoginRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:create')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class Payment(DispatchLoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/payment.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'order'


class SaveOrder(View):
    template_name = 'order/payment.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:create')

        if not self.request.session.get('cart'):
            messages.error(self.request,
                           'Seu carrinho está vazio')

        cart = self.request.session.get('cart')
        total = utils.cart_total(cart)
        items = utils.total_items(cart)
        cart_variations = [v for v in cart]
        variations_bd = Variation.objects.filter(id__in=cart_variations)

        for variation in variations_bd:
            vid = str(variation.pk)
            # variation_bd = Variation.objects.get(id=int(variation))
            cart_quantity = cart[vid]['quantity']
            unit_price = cart[vid]['unit_price']
            promotional_unit_price = cart[vid]['promotional_unit_price']
            variation_stock = variation.stock

            if cart_quantity > variation_stock:
                cart[vid]['quantity'] = variation_stock

                cart[vid]['quant_price'] = unit_price * variation_stock
                cart[vid]['promotional_quant_price'] = promotional_unit_price * \
                    variation_stock

                messages.error(self.request,
                               'Alguns produtos do seu carrinho excederam o limite de nosso estoque! Verifique os itens que foram alterados\
                                   e se quiser, prossiga com a compra')

                self.request.session.save()
                return redirect('product:cart')

        order = Order(
            user=self.request.user,
            total=total,
            quantity_items=items,
            status='C'
        )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=variant['product_name'],
                    product_id=variant['product_id'],
                    variation=variant['variation_name'],
                    variation_id=variant['variation_id'],
                    price=variant['quant_price'],
                    promotional_price=variant['promotional_quant_price'],
                    quantity=variant['quantity'],
                    image=variant['image'],
                ) for variant in cart.values()
            ]
        )

        for variant in cart.values():
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print('------------------------------')
            print(variant['variation_name'])

        del self.request.session['cart']
        return render(self.request, self.template_name)


class Details(View):
    pass
