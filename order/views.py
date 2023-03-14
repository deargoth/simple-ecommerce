from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from utils import ec_messages, utils
from .models import Order, OrderItems


class SaveOrder(View):
    def get(self, *args, **kwargs):

        if not self.request.session.get('cart'):
            messages.error(self.request,
                           ec_messages.error_cart_empty)
            return redirect('product:index')

        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           ec_messages.error_login_required)
            return redirect('profile:login')

        cart = self.request.session.get('cart')
        quant_items = utils.total_items_in_cart(cart)
        total_cart = utils.cart_total_value(cart)

        pid_keys = []
        vid_keys = []

        order = Order.objects.create(
            user=self.request.user,
            total_items=quant_items,
            total_value=total_cart,
            status='C'
        )

        order.save()

        OrderItems.objects.bulk_create(
            [
                OrderItems(
                    order=order,
                    product=cart[value]['product_name'],
                    product_id=cart[value]['product_id'],
                    price=cart[value]['unit_price'],
                    promotional_price=cart[value]['promotional_unit_price'],
                    image=cart[value]['image'],
                    quantity=cart[value]['quantity'],
                    slug=cart[value]['slug'],
                )
                for value in pid_keys
                if pid_keys
            ],
        )

        OrderItems.objects.bulk_create(
            [
                OrderItems(
                    order=order,
                    product=cart[value]['product_name'],
                    product_id=cart[value]['product_id'],
                    variation=cart[value]['variation_name'],
                    variation_id=cart[value]['variation_id'],
                    price=cart[value]['unit_price'],
                    promotional_price=cart[value]['promotional_unit_price'],
                    image=cart[value]['image'],
                    quantity=cart[value]['quantity'],
                    slug=cart[value]['slug'],
                )
                for value in vid_keys
                if vid_keys
            ]
        )

        del self.request.session['cart']
        messages.add_message(self.request,
                             ec_messages.success_order_created)
        return redirect('product:resume')
