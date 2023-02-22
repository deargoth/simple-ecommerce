from django.template import Library
from utils import utils

register = Library()


@register.filter(name="currency")
def currency(value):
    return utils.currency(value)


@register.filter(name="total_items")
def total_items(cart):
    return utils.total_items(cart)


@register.filter(name="cart_total")
def cart_total(cart):
    return utils.cart_total(cart)
