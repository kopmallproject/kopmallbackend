import re

from accounts.models import User

def validate_password(password):
    
    message = "password should contain uppercase, lowercase, numbers and symbols"
    
    if len(password) < 8:
        raise ValueError("password should not be less than 8")
    
    if not re.search(r'[A-Z]', password):
        raise ValueError(message)
    if not re.search(r'[a-z]', password):
        raise ValueError(message)
    if not re.search(r'\d', password):
        raise ValueError(message)
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError(message)
    
    return password

def validate_email(email):
    user = User.objects.filter(email__iexact=email).exists()

    if user:
        raise ValueError("choose another email")
    return email


# def validate(self, validated_data):
#     order_quantity = validated_data["quantity"]
#     product_quantity = validated_data["product"].quantity

#     order_id = self.context["view"].kwargs.get("order_id")
#     product = validated_data["product"]
#     current_item = OrderItem.objects.filter(order__id=order_id, product=product)

#     if order_quantity > product_quantity:
#         error = {"quantity": _("Ordered quantity is more than the stock.")}
#         raise serializers.ValidationError(error)

#     if not self.instance and current_item.count() > 0:
#         error = {"product": _("Product already exists in your order.")}
#         raise serializers.ValidationError(error)

#     return validated_data