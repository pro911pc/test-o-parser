import uuid
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import ProductPostSerializer, ProductSerializer
from api.tasks import get_content_product
from products.models import Product, ProductPost


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        products_count = request.data.get('products_count')
        current_datetime = datetime.now(tz=timezone.utc)
        id_request = uuid.uuid4()
        get_content_product.apply_async((products_count, id_request))
        ProductPost.objects.create(products_count=products_count,
                                   created=current_datetime,
                                   id_request=id_request)
        return Response("Обработка начата")

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductPostSerializer
        return ProductSerializer
