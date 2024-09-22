from functools import cached_property
from xml.etree.ElementInclude import default_loader
from django.db import models

from core.models import BaseModel
from stores.models.store_model import Product
from django.utils.translation import gettext_lazy as _


from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(BaseModel):
    user = models.ForeignKey(User, related_name="user_cart", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="cart_product",
    )
    
    quantity = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.product.name} -- {self.pk}"

    @cached_property
    def subtotal(self):
        """
        Total cost of the ordered item
        """
        return round(self.quantity * self.product.amount, 2)