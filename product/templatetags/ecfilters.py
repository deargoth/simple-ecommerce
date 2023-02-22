from django.template import Library
from utils import utils

register = Library()


@register.filter(name="currency")
def currency(value):
    return utils.currency(value)
