from django.db import models
from django.core.validators import MaxValueValidator


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    price = models.IntegerField(
        verbose_name='Цена'
    )
    description = models.CharField(
        max_length=200,
        verbose_name='описание'
    )
    image_url = models.CharField(
        max_length=200,
        verbose_name='Изображение товара'
    )
    discount = models.CharField(
        max_length=200,
        verbose_name='скидка',
        null=True,
    )


class ProductPost(models.Model):
    products_count = models.IntegerField(
        default=10,
        validators=[MaxValueValidator(50)]
    )
