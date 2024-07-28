from typing import Type, Dict

from ninja import Schema, ModelSchema
from ninja_jwt.schema import TokenObtainInputSchemaBase

from pydantic import EmailStr, field_validator

from accounts.validator import validate_password, validate_email
from accounts.models import User
from core.helpers import get_tokens


class UserInSchema(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    password: str

    _validate_password = field_validator("password")(validate_password)
    _validate_email = field_validator("email")(validate_email)


class UserOutSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ["groups", "password", "is_superuser", "is_staff", "user_permissions"]


class CreateUserOutSchema(UserOutSchema):
    token: dict

    @staticmethod
    def resolve_token(obj):
        if not obj:
            return
        return get_tokens(obj)


class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str

class MyTokenObtainPairInputSchema(TokenObtainInputSchemaBase):
    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return MyTokenObtainPairOutSchema

    @classmethod
    def get_token(cls, user) -> Dict:
        return get_tokens(user)  # type: ignore

class GetOTPInSchema(Schema):
    email: EmailStr

class VerifyOTPOutSchema(Schema):
    email: EmailStr
    otp: str

class ResetPasswordInSchema(Schema):
    email: EmailStr
    password: str
    confirm_password: str

    _validate_password = field_validator("password")(validate_password)