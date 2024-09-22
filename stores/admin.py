from django.contrib import admin

from stores.models.store_model import Product, ProductImage, Category, SubCategory
from stores.models.cart_model import Cart
from stores.models.order_model import Order, OrderItem

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)

