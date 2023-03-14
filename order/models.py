from django.db import models
from userprofile.models import CustomUser


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    total_items = models.PositiveIntegerField()
    total_value = models.FloatField()
    status = models.CharField(
        max_length=1,
        default='C',
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        ),
    )

    def __str__(self):
        return f'Pedido N° {self.pk}'


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=255, blank=True, null=True)
    variation_id = models.PositiveIntegerField(blank=True, null=True)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)
    slug = models.CharField(max_length=265)

    def __str__(self):
        return f'Item do pedido {self.order.pk}'

    class Meta:
        verbose_name = 'Order item'
        verbose_name_plural = 'Order itens'
