from django.db import models
from django.utils.text import slugify
from django.conf import settings
from PIL import Image
from utils import utils


class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    long_description = models.TextField()
    image = models.ImageField(upload_to='img/%Y/%m')
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    slug = models.SlugField(unique=True, blank=True, null=True)
    stock = models.PositiveIntegerField(default=1)
    type = models.CharField(
        max_length=1,
        default='S',
        choices=(
            ('S', 'Simples'),
            ('V', 'Variável'),
        )
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)

        if self.image:
            utils.resize_image(self.image)

    def __str__(self):
        return self.name


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(
        upload_to='variation/%Y/%m', blank=True, null=True)
    promotional_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            utils.resize_image(self.image)

    def __str__(self):
        return self.name or self.product.name
