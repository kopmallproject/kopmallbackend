from ninja import ModelSchema

from stores.models.cart_model import Cart
from stores.schemas.store_schema import ProductOutSchema

class CartOutSchema(ModelSchema):
    product: ProductOutSchema
    subtotal: float = 0
    
    class Meta:
        model = Cart
        fields = (
            "id",
            "product",
            "quantity",
            "date_updated",
            "date_created",
        )
