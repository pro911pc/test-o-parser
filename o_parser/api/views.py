from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse
from products.models import Product
from api.tasks import get_content_product

from api.serializers import ProductSerializer, ProductPostSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        #get_content_product.delay(request.data.get('products_count'))
        get_content_product(request.data.get('products_count'))
        return Response("Обработка начата")

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductPostSerializer
        return ProductSerializer
