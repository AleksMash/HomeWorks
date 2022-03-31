from django.contrib import admin
from .models import Product, ProductOrder, Staff, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductOrder)
admin.site.register(Staff)
admin.site.register(Order)
