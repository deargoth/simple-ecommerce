import re
import locale
from django.conf import settings
from PIL import Image


def resize_image(img, new_width=800):
    img_full_path = settings.MEDIA_ROOT / img.name
    img_pil = Image.open(img_full_path)
    original_width, original_height = img_pil.size

    if original_width <= new_width:
        img_pil.close()
        return

    new_height = round((new_width * original_height) / original_width)

    new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
    new_img.save(
        img_full_path,
        optimize=True,
        quality=50
    )


def currency(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valor = locale.currency(value, grouping=True, symbol=None)
    return f'R${valor}'


def cart_total_value(cart):
    return sum(
        [
            price['promotional_quant_price']
            if
            price['promotional_quant_price']
            else
            price['quant_price']
            for price
            in cart.values()
        ]
    )


def total_items_in_cart(cart):
    return sum(
        [
            item['quantity']
            for item
            in cart.values()
        ]
    )


def valida_cpf(cpf):
    cpf = str(cpf)
    cpf = re.sub(r'[^0-9]', '', cpf)

    if not cpf or len(cpf) != 11:
        return False

    # Elimina os dois últimos digitos do CPF
    novo_cpf = cpf[:-2]
    reverso = 10                        # Contador reverso
    total = 0

    # Loop do CPF
    for index in range(19):
        if index > 8:                   # Primeiro índice vai de 0 a 9,
            index -= 9                  # São os 9 primeiros digitos do CPF

        # Valor total da multiplicação
        total += int(novo_cpf[index]) * reverso

        reverso -= 1                    # Decrementa o contador reverso
        if reverso < 2:
            reverso = 11
            d = 11 - (total % 11)

            if d > 9:                   # Se o digito for > que 9 o valor é 0
                d = 0
            total = 0                   # Zera o total
            novo_cpf += str(d)          # Concatena o digito gerado no novo cpf

    # Evita sequencias. Ex.: 11111111111, 00000000000...
    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

    # Descobri que sequências avaliavam como verdadeiro, então também
    # adicionei essa checagem aqui
    if cpf == novo_cpf and not sequencia:
        return True
    else:
        return False
