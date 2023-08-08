from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse
from products.models import Product, ProductPost
from api.tasks import get_content_product
from datetime import datetime
from django.utils import timezone
import uuid

from api.serializers import ProductSerializer, ProductPostSerializer


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
