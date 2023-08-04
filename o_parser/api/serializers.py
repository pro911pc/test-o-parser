from rest_framework import serializers
from django.core.validators import MaxValueValidator
from products.models import Product, ProductPost


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')


class ProductPostSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(
        default=10,
        validators=[MaxValueValidator(50)]
    )

    def validate_products_count(self, value):
        if value > 50:
            raise serializers.ValidationError("Максимальное значение products_count 50")
        return value

    class Meta:
        model = ProductPost
        fields = ('__all__')
