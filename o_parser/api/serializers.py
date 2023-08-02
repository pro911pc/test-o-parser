from rest_framework import serializers

from products.models import Product, ProductPost


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')


class ProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPost
        fields = ('__all__')
