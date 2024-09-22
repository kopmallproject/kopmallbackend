import secrets
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from accounts.models import Address
from core.models import BaseModel
from stores.models.store_model import Product


User = get_user_model()

def get_random_ids():
    return "".join([str(secrets.randbelow(10)) for _ in range(10)])
    
class Order(BaseModel):
    PENDING = "PENDING"
    ONGOING = "ONGOING"
    DELIVERED = "DELIVERED"
    CLOSED = "CLOSED"

    STATUS_CHOICES = (
        (PENDING, _("pending")), 
        (ONGOING, _("ongoing")),
        (DELIVERED, _("delivered")),
        (CLOSED, _("closed")),
    )

    buyer = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=PENDING)
    order_id = models.CharField(max_length=15, default=get_random_ids)
    shipping_address = models.ForeignKey(
        Address,
        related_name="shipping_orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.buyer.get_full_name()

    @cached_property
    def total_cost(self):
        """
        Total cost of all the items in an order
        """
        return round(sum([order_item.cost for order_item in self.order_items.all()]), 2) # type: ignore


class OrderItem(BaseModel):

    PENDING = "PENDING"
    ONGOING = "ONGOING"
    DELIVERED = "DELIVERED"
    CLOSED = "CLOSED"
    REFUNDED = "REFUNDED"

    STATUS_CHOICES = (
        (PENDING, _("pending")), 
        (ONGOING, _("ongoing")),
        (DELIVERED, _("delivered")),
        (CLOSED, _("closed")),
        (REFUNDED, _("refunded"))
    )

    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="product_orders", on_delete=models.CASCADE
    )
    orderitem_id = models.CharField(max_length=15, default=get_random_ids)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=PENDING)
    
    quantity = models.IntegerField()

    def __str__(self):
        return self.order.buyer.get_full_name()

    @cached_property
    def cost(self):
        """
        Total cost of the ordered item
        """
        return round(self.quantity * self.product.amount, 2)