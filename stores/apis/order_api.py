from core.schema import NOTFOUND_404OUTSCHEMA
from stores.models.order_model import Order, OrderItem


from typing import List

from ninja import Router

from stores.schemas.order_schema import OrderItemOutSchema, OrderOutSchema

router = Router()


@router.get(
    "/",
    description="The endpoint that queries all orders under a user",
    response={200: List[OrderOutSchema]},
)
def list_orders(request):
    user = request.user
    orders = Order.objects.select_related("buyer", "shipping_address__user").filter(
        buyer=user
    )
    return orders

@router.get(
    "{order_id}/",
    description="The endpoint that queries a single order under a user",
    response={200: OrderOutSchema, 404: NOTFOUND_404OUTSCHEMA} 
)
def get_order(request, order_id: int):

    order = Order.objects.select_related("buyer", "shipping_address__user").filter(
        pk=order_id
    ).first()

    if not order:
        return 404, {'message': "Order is not available"}
    
    return order

@router.get(
    "/{order_id}/orderitems/",
    description="The endpoint that queries a ordered items under an order",
    response={200: List[OrderItemOutSchema]},
)
def list_orderitems(request, order_id: int):
    orderitem = OrderItem.objects.select_related(
        "order__buyer", "order__shipping_address__user", "product__category"
    ).filter(order_id=order_id)

    return orderitem
