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
            vid_cart_key = f'vid_{vid}'

            variation = Variation.objects.get(id=vid)
            variation_stock = variation.stock
            product = variation.product

            product_name = product.name
            product_id = product.pk
            variation_name = variation.name
            variation_id = variation.pk
            variation_price = variation.price
            variation_promotional_price = variation.promotional_price

            if variation.image:
                variation_image = variation.image.name
            else:
                variation_image = product.image.name

            slug = product.slug
            quantity = 1

            if vid_cart_key not in cart.keys():
                cart[vid_cart_key] = {
                    'product_name': product_name,
                    'product_id': product_id,
                    'variation_name': variation_name,
                    'variation_id': variation_id,
                    'unit_price': variation_price,
                    'promotional_unit_price': variation_promotional_price,
                    'quant_price': variation_price,
                    'promotional_quant_price': variation_promotional_price,
                    'slug': slug,
                    'quantity': 1,
                    'image': variation_image,
                }

            else:
                cart_quantity = cart[vid_cart_key]['quantity']
                product_stock = variation_stock
                unit_price = cart[vid_cart_key]['unit_price']
                promotional_unit_price = cart[vid_cart_key]['promotional_unit_price']
                cart_quantity += 1

                if cart_quantity >= product_stock:
                    messages.error(self.request,
                                   ec_messages.error_quantity_exceeded)
                    cart_quantity = product_stock

                cart[vid_cart_key]['quantity'] = cart_quantity
                cart[vid_cart_key]['quant_price'] = unit_price * cart_quantity
                cart[vid_cart_key]['promotional_quant_price'] = promotional_unit_price * cart_quantity

        elif 'pid' in self.request.GET.keys():
            pid = self.request.GET.get('pid')
            pid_cart_key = f'pid_{pid}'

            product = Product.objects.get(id=pid)
            db_stock = product.stock

            product_name = product.name
            product_id = product.pk
            product_price = product.price
            product_promotional_price = product.promotional_price
            image = product.image.name
            slug = product.slug

            if pid_cart_key not in cart.keys():
                cart[pid_cart_key] = {
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
                cart_quantity = cart[pid_cart_key]['quantity']
                product_stock = db_stock
                unit_price = cart[pid_cart_key]['unit_price']
                promotional_unit_price = cart[pid_cart_key]['promotional_unit_price']
                cart_quantity += 1

                if cart_quantity >= product_stock:
                    messages.error(self.request,
                                   ec_messages.error_quantity_exceeded)
                    cart_quantity = product_stock

                cart[pid_cart_key]['quantity'] = cart_quantity
                cart[pid_cart_key]['quant_price'] = unit_price * cart_quantity
                cart[pid_cart_key]['promotional_quant_price'] = promotional_unit_price * cart_quantity

        self.request.session.save()

        return redirect(http_referer)


class Cart(View):
    template_name = 'product/cart.html'

    def get(self, *args, **kwargs):
        cart = self.request.session.get('cart')

        self.context = {
            'cart': cart,
        }

        return render(self.request, self.template_name, self.context)


class DelFromCart(View):
    def get(self, *args, **kwargs):
        if not self.request.session.get('cart'):
            messages.error(self.request,
                           ec_messages.error_cart_empty)
            return redirect('product:index')

        cart = self.request.session.get('cart')
        name = self.kwargs.get('name')

        variation = Variation.objects.filter(name__exact=name).first()
        product = Product.objects.filter(name__exact=name).first()

        if variation:
            pk = f'vid_{variation.pk}'

        if product:
            pk = f'pid_{product.pk}'

        item_quantity_cart = cart[pk]['quantity']

        unit_price = cart[pk]['unit_price']
        promotional_unit_price = cart[pk]['promotional_unit_price']

        item_quantity_cart -= 1
        cart[pk]['quant_price'] = unit_price * item_quantity_cart
        cart[pk]['promotional_quant_price'] = promotional_unit_price * \
            item_quantity_cart
        cart[pk]['quantity'] = item_quantity_cart

        if item_quantity_cart <= 0:
            cart.pop(pk)

        self.request.session.save()
        return redirect('product:cart')


class Resume(View):
    template_name = 'product/resume.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           ec_messages.error_login_needed)
            return redirect('profile:login')

        if not self.request.session.get('cart'):
            messages.error(self.request,
                           ec_messages.error_cart_empty)
            return redirect('product:index')

        self.context = {
            'cart': self.request.session.get('cart'),
            'user': self.request.user,
        }

        return render(self.request, self.template_name, self.context)
