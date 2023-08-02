from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ProductsViewSet

app_name = 'api'

router = DefaultRouter()
router.register('products', ProductsViewSet, basename='product')

urlpatterns = [
    path('v1/', include(router.urls)),
]
