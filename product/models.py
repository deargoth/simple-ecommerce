from django.db import models
from django.template.defaultfilters import slugify
from PIL import Image
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    long_description = models.TextField()
    image = models.ImageField(
        upload_to='product_imgs/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    marketing_price = models.FloatField()
    promotional_marketing_price = models.FloatField(default=0)
    type = models.CharField(
        max_length=1,
        default='V',
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    @staticmethod
    def resize_image(img, new_width):
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
            quality=50,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        max_image_size = 800

        if self.image:
            self.resize_image(self.image, max_image_size)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Variation(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f'Variação {self.name} - {self.product}'
