from utils import utils
from django.template import Library

register = Library()


@register.filter
def currency(value):
    return utils.currency(value)


@register.filter
def cart_total_value(cart):
    return utils.cart_total_value(cart)


@register.filter
def total_items_in_cart(cart):
    return utils.total_items_in_cart(cart)
