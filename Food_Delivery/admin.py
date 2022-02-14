
from django.contrib import admin
from .models import Product
from .models import OrderItem
from .models import Customer
from .models import Order
from .models import ShipppingAddress



admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(ShipppingAddress)
