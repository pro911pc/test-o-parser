from django.db import models
from django.core.validators import MaxValueValidator


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    url = models.CharField(
        max_length=200,
        verbose_name='Страница продукта'
    )


class ProductPost(models.Model):
    products_count = models.IntegerField(
        default=10,
        validators=[MaxValueValidator(50)]
    )
