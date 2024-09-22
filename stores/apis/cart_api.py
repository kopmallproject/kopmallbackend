from core.schema import NOTFOUND_404OUTSCHEMA, SUCCESS_204OUTSCHEMA
from stores.models.cart_model import Cart


from typing import List

from ninja import Router

from stores.schemas.cart_schema import CartOutSchema


router = Router()


@router.get(
    "/",
    description="The endpoint that queries user cart",
    response={200: List[CartOutSchema]},
)
def list_carts(request):
    user = request.user
    carts = Cart.objects.select_related("user", "product__category").filter(
        user=user
    )
    return carts

@router.delete(
    "/{cart_id}/delete/",
    description="The endpoint that remove user cart",
    response={204: SUCCESS_204OUTSCHEMA, 404: NOTFOUND_404OUTSCHEMA},
)
def delete_cart(request, cart_id: int):
    cart = Cart.objects.select_related("user", "product__category").filter(
        pk=cart_id
    ).first()
    if not cart:
        return 404, {'message': "Product is not available"}
    else:
        cart.delete()
        
    return 204, {'message': "Product removed successfully"}