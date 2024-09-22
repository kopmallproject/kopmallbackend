from accounts.schema import AddressOutSchema
from stores.models.order_model import Order, OrderItem

from ninja import ModelSchema

from stores.schemas.store_schema import ProductOutSchema

class OrderItemOutSchema(ModelSchema):
    product: ProductOutSchema
    cost: float = 0.0
    
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "quantity",
            "orderitem_id",
            "date_updated",
            "date_created",
        )


class OrderOutSchema(ModelSchema):
    total_cost: float = 0.0
    shipping_address: AddressOutSchema
    
    class Meta:
        model = Order
        fields = (
            "id",
            "shipping_address",
            "status",
            "order_id",
            "date_updated",
            "date_created",
        )







# class OrderWriteSerializer(serializers.ModelSerializer):
#     """
#     Serializer class for creating orders and order items

#     Shipping address, billing address and payment are not included here
#     They will be created/updated on checkout
#     """

#     buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     order_items = OrderItemSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = (
#             "id",
#             "buyer",
#             "status",
#             "order_items",
#             "created_at",
#             "updated_at",
#         )
#         read_only_fields = ("status",)

#     def create(self, validated_data):
#         orders_data = validated_data.pop("order_items")
#         order = Order.objects.create(**validated_data)

#         for order_data in orders_data:
#             OrderItem.objects.create(order=order, **order_data)

#         return order

#     def update(self, instance, validated_data):
#         orders_data = validated_data.pop("order_items", None)
#         orders = list((instance.order_items).all())

#         if orders_data:
#             for order_data in orders_data:
#                 order = orders.pop(0)
#                 order.product = order_data.get("product", order.product)
#                 order.quantity = order_data.get("quantity", order.quantity)
#                 order.save()

#         return instance