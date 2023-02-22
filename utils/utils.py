import locale


def currency(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    value = locale.currency(value, grouping=True, symbol=None)
    return f'R${value}'


def total_items(cart):
    return sum(
        [item['quantity']
         for item
         in cart.values()
         ]
    )


def cart_total(cart):
    return sum(
        [
            value['promotional_quant_price']
            if value['promotional_quant_price']
            else
            value['quant_price']
            for value in cart.values()
        ]
    )
