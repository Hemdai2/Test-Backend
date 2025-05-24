from django.contrib import admin

from .models import Order, OrderItem, Flavor, Tub

# Register your models here.
admin.site.register(Flavor)
admin.site.register(Tub)
admin.site.register(Order)
admin.site.register(OrderItem)
