from django.contrib import admin

from stores.models import Product, ProductImage, Category, SubCategory

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(SubCategory)
