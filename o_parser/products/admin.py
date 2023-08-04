from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'price',
                    'description',
                    'image_url',
                    'discount')
    search_fields = ('name', 'description')
    empty_value_display = '-пусто-'


admin.site.register(Product, ProductAdmin)
