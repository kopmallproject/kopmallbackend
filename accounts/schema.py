from ninja import Schema, ModelSchema

from pydantic import EmailStr, field_validator

from accounts.validator import validate_password, validate_email
from accounts.models import User


class UserInSchema(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    password: str

    _validate_password = field_validator('password')(validate_password)
    _validate_email = field_validator('email')(validate_email)



class UserOutSchema(ModelSchema):
    class Meta:
        model = User
        exclude = [
            "groups",
            "password",
            "is_superuser",
            "is_staff",
            "user_permissions"
        ]

class ERROR_403OUTSCHEMA(Schema):
    error: str