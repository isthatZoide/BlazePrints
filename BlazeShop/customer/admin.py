from django.contrib import admin
from .models import CatalogueItem, Category, OrderModel


admin.site.register(CatalogueItem)
admin.site.register(Category)
admin.site.register(OrderModel)
